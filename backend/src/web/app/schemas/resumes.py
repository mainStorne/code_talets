from pydantic import BaseModel

class Resume(BaseModel):
    resume_url: str


class ResumeRead(Resume):
    user_id: int


