from pydantic import BaseModel

class DiaryRequest(BaseModel):
    content: str