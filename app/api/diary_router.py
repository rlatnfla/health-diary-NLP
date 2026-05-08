from fastapi import APIRouter
from app.schemas.diary_schema import DiaryRequest
from nlp.extractor import get_extractor

router = APIRouter()
extractor = get_extractor()

@router.post("/analyze")
async def analyze_diary(request: DiaryRequest):
    result = await extractor.extract(request.content)
    return result