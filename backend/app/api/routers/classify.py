from fastapi import APIRouter, HTTPException
from typing import Union
from app.models.schemas import (
    ClassificationQuestion,
    ClassificationAnswerRequest,
    ClassificationResult
)
from app.services.classification_service import classification_service

router = APIRouter(prefix="/api/classify", tags=["Product Classification"])

@router.get("/start", response_model=ClassificationQuestion)
def start_classification():
    """Start the 6-category AYUSH product classification wizard."""
    return classification_service.start_classification()

@router.post("/answer", response_model=Union[ClassificationQuestion, ClassificationResult])
def submit_answer(req: ClassificationAnswerRequest):
    """Submit an answer to a classification question and get the next question or final category result."""
    result = classification_service.submit_answer(req.question_id, req.option_id)
    return result
