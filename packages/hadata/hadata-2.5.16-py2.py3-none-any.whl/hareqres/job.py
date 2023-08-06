from typing import Optional, List

from pydantic import BaseModel


class Job(BaseModel):
    name: str
    filename: str
    file_hash: str
    status: str
    transcript: str


class JobHistory(BaseModel):
    job_id: str
    job_status: str
    status_date_time: str


class Transcript(BaseModel):
    transcript: str