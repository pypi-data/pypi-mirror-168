from typing import Optional, List
from pydantic import BaseModel


class QuestionAnswerEditRequest(BaseModel):
    job_id: Optional[str]
    question: Optional[str]
    answer: Optional[str]
    skill_id: Optional[str]
    subskill_1_id: Optional[str]
    subskill_2_id: Optional[str]
    subskill_3_id: Optional[str]
    level_id: Optional[str]
    question_type: Optional[str]
    question_theme: Optional[str]
    time: Optional[str]
    points: Optional[int]
    media_question: Optional[bool]
    media_extension: Optional[str]
    file_encoded: Optional[str]
    roles: Optional[List[str]]


class QuestionSearch(BaseModel):
    question_title: Optional[str] = None
    skill_id: Optional[str] = None
    level_id: Optional[str] = None
    subskill_1_id: Optional[str] = None
    subskill_2_id: Optional[str] = None
    subskill_3_id: Optional[str] = None
    role_id: Optional[str] = None
