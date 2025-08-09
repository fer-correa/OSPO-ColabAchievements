from sqlmodel import Session, select
from .models import Contributor, Achievement

def get_contributor_by_username(db: Session, username: str) -> Contributor | None:
    statement = select(Contributor).where(Contributor.github_username == username)
    return db.exec(statement).first()

def create_contributor(db: Session, contributor: Contributor) -> Contributor:
    db.add(contributor)
    db.commit()
    db.refresh(contributor)
    return contributor

def get_achievement_by_source_url(db: Session, source_url: str) -> Achievement | None:
    statement = select(Achievement).where(Achievement.source_contribution_url == source_url)
    return db.exec(statement).first()

def create_achievement_for_contributor(db: Session, achievement: Achievement) -> Achievement:
    db.add(achievement)
    db.commit()
    db.refresh(achievement)
    return achievement
