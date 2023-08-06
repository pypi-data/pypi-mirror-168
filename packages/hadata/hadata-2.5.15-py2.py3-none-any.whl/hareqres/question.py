from typing import Optional, List

from pydantic import BaseModel


class QuestionAnswer(BaseModel):
    job_id: str
    question: str
    answer: str
    skill_id: Optional[str]
    level_id: Optional[str]
    subskill_1_id: Optional[str]
    subskill_2_id: Optional[str]
    subskill_3_id: Optional[str]
    question_type: str
    question_theme: Optional[str]
    time: str
    points: int
    media_question: Optional[bool]
    media_extension: Optional[str]
    file_encoded: Optional[str]
    roles: Optional[List[str]]
