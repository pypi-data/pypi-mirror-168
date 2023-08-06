from datetime import date

from pydantic import BaseModel


class Assessments(BaseModel):
    type: str
    title: str
    start_date: date
    end_date: date
    is_active: bool
    description: str


class AssessmentsQuestionAnswer(BaseModel):
    sort_order: int
    question_answer_id: str
    assessment_id: str


class AssessmentsSettings(BaseModel):
    assessment_id: str
    show_score: bool
    shuffle_questions: bool
    enable_copy: bool
    attempt_count: int
    custom_message: str


class AssessmentsUser(BaseModel):
    user_id: str
    assessment_id: str
    score: int
    enabled: bool
    status: str



