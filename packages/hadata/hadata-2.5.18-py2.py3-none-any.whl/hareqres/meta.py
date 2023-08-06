from typing import Optional

from pydantic import BaseModel


class Level(BaseModel):
    level_name: str
    level_description: str


class Role(BaseModel):
    role_name: str
    role_description: str


class Skill(BaseModel):
    skill_name: str
    skill_description: str


class Subskill(BaseModel):
    subskill_name: str
    parent_skill_id: str
    parent_skill_name: Optional[str]


class TranscriptFilter(BaseModel):
    job_id: str
    start_position: int
    end_position: int
    status: str
