from typing import List

from pydantic import BaseModel


class QuestionAnswerLoad(BaseModel):
    question_answer_id: str
    job_id: str
    question: str
    answer: str
    skill_id: str
    level_id: str
    question_type: str
    question_theme: str
    organization_id: str
    time: str
    points: str


class AssessmentUserGet(BaseModel):
    assessment_user_id: str
    user_id: str
    score: int
    enabled: bool
    status: str


class AssessmentSettingsGet(BaseModel):
    assessment_settings_id: str
    show_score: bool
    shuffle_questions: bool
    enable_copy: bool
    attempt_count: int
    custom_message: str


class AssessmentGet(BaseModel):
    assessment_id: str
    assessment_title: str
    assessment_type: str
    description: str
    start_date: str
    end_date: str
    is_active: bool
    organization_id: str
    creation_date_time: str


class AssessmentUserFull(BaseModel):
    assessment_user: AssessmentUserGet
    assessment_settings: AssessmentSettingsGet
    assessment: AssessmentGet


class AssessmentUserFullList(BaseModel):
    assessment_details: List[AssessmentUserFull]
