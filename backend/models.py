from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

class AchievementBase(SQLModel):
    title: str
    description: str
    awarded_at: datetime = Field(default_factory=datetime.utcnow)
    source_contribution_url: Optional[str] = Field(default=None, unique=True)

class Achievement(AchievementBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contributor_id: int = Field(foreign_key="contributor.id")
    contributor: "Contributor" = Relationship(back_populates="achievements")

class AchievementCreate(AchievementBase):
    pass

class AchievementRead(AchievementBase):
    id: int

class ContributorBase(SQLModel):
    github_username: str = Field(index=True, unique=True)
    avatar_url: str

class Contributor(ContributorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    achievements: List[Achievement] = Relationship(back_populates="contributor")

class ContributorCreate(ContributorBase):
    pass

class ContributorRead(ContributorBase):
    id: int

class ContributorReadWithAchievements(ContributorRead):
    achievements: List[AchievementRead] = []
