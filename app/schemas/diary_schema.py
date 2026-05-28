from pydantic import BaseModel, Field


class DiaryRequest(BaseModel):
    content: str = Field(..., description="사용자가 작성한 일일 일기 본문 텍스트")
