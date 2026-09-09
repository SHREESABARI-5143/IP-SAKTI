from fastapi import APIRouter
from backend.app.schemas.classification import ClassificationInput, ClassificationResult
from backend.app.agents.classification_agent import classification_agent

router = APIRouter(prefix="/classify", tags=["Formulation Classification Engine"])

@router.post("", response_model=ClassificationResult)
async def classify_product(data: ClassificationInput):
    return classification_agent.classify(data)
