from datetime import date

from pydantic import BaseModel


class AssessmentQNASortOrder(BaseModel):
    assessment_qna_id: str
    sort_order: str


class AssessmentCreation(BaseModel):
    type: str
    title: str
    start_date: date
    end_date: date
    description: str


class AssessmentStatusChange(BaseModel):
    assessment_id: str
    is_active: bool


class AssessmentUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    assessment_id: str
    enabled: bool
    score: int
    status: str


class AssessmentUserAddRequest(BaseModel):
    email: str
    assessment_id: str
    enabled: bool
    score: int
    status: str


class AssessmentUserStatusRequest(BaseModel):
    assessment_user_id: str
    enabled: bool


class UserAssessmentMarkedRequest(BaseModel):
    assessment_user_id: str
    marked: bool


class UserAssessmentQNAMarkedRequest(BaseModel):
    assessment_user_qna_id: str
    is_correct: bool
    personal_notes: str
