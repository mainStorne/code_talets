from pydantic import BaseModel

class Resume(BaseModel):
    resume_url: str


class ResumeRead(BaseModel):
    user_id: int


