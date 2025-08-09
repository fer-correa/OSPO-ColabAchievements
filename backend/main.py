from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import Session

from . import crud
from .database import create_db_and_tables, engine
from .models import Contributor, ContributorCreate, ContributorRead, ContributorReadWithAchievements, Achievement, AchievementCreate, AchievementRead

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="OSPO-ColabAchievements API",
    version="0.1.0",
    description="API for tracking and generating achievements for open source contributors.",
    lifespan=lifespan
)

# CORS Middleware
origins = [
    "http://localhost",
    "http://localhost:5173",  # Default Vite dev server port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    with Session(engine) as session:
        yield session

@app.get("/")
def read_root():
    return {"message": "Welcome to the OSPO-ColabAchievements API"}

@app.post("/contributors/", response_model=ContributorRead)
def create_contributor(contributor: ContributorCreate, db: Session = Depends(get_db)):
    db_contributor = crud.get_contributor_by_username(db, username=contributor.github_username)
    if db_contributor:
        raise HTTPException(status_code=400, detail="Contributor already registered")
    return crud.create_contributor(db=db, contributor=Contributor.from_orm(contributor))

@app.get("/contributors/{username}/", response_model=ContributorReadWithAchievements)
def read_contributor(username: str, db: Session = Depends(get_db)):
    db_contributor = crud.get_contributor_by_username(db, username=username)
    if db_contributor is None:
        raise HTTPException(status_code=404, detail="Contributor not found")
    return db_contributor

@app.post("/contributors/{username}/achievements/", response_model=AchievementRead)
def create_achievement_for_contributor(username: str, achievement: AchievementCreate, db: Session = Depends(get_db)):
    db_contributor = crud.get_contributor_by_username(db, username=username)
    if db_contributor is None:
        raise HTTPException(status_code=404, detail="Contributor not found")
    
    # Check if achievement already exists for this source URL
    existing_achievement = crud.get_achievement_by_source_url(db, source_url=achievement.source_contribution_url)
    if existing_achievement:
        # Optionally, raise HTTPException(status_code=409, detail="Achievement already exists")
        # For now, just return the existing one to make worker idempotent
        print(f"Achievement for source URL {achievement.source_contribution_url} already exists. Skipping creation.")
        return existing_achievement

    achievement_to_create = Achievement(**achievement.dict(), contributor_id=db_contributor.id)
    return crud.create_achievement_for_contributor(db=db, achievement=achievement_to_create)
