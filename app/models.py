# app/models.py

from pydantic import Field, BaseModel

class SupportAnswer(BaseModel):

    answer: str
    confidence: float = Field(ge = 0, le = 1)
    needs_human: bool
    