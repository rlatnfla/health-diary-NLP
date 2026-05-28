from fastapi import APIRouter, status

from app.schemas.diary_schema import DiaryRequest
from nlp.extractor import get_extractor

router = APIRouter()
extractor = get_extractor()


@router.post("/analyze", status_code=status.HTTP_200_OK)
async def analyze_diary(request: DiaryRequest):
    result = await extractor.extract(request.content)
    return result
