from typing import Optional

from pydantic import BaseModel, constr, EmailStr


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    organization_id: str
    profile_type: str


class PasswordUpdate(BaseModel):
    password: str


class ResendEmail(BaseModel):
    email: str


class User(BaseModel):
    first_name: Optional[constr(min_length=1, max_length=50)]
    last_name: Optional[constr(min_length=1, max_length=50)]
    email: Optional[EmailStr]
    password: Optional[constr(min_length=4)]
    organization_id: Optional[str]
    profile_type: Optional[int]
    is_verified: Optional[bool] = False


class UserProfile(BaseModel):
    role: str
    focus_area: str
    projects: list


class UserAssessments(BaseModel):
    skill: str
    level: str
    due_date: str
    score: str


class UserObjectives(BaseModel):
    sample_field: str


class UserAssessmentsQuestionAnswer(BaseModel):
    question_answer_id: str
    assessment_id: str


class Token(BaseModel):
    token: str
