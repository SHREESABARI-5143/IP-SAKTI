from fastapi import APIRouter
from backend.app.schemas.abs import ABSAssessmentInput, ABSAssessmentResult
from backend.app.agents.abs_agent import abs_agent

router = APIRouter(prefix="/abs", tags=["Access and Benefit Sharing (ABS) Engine"])

@router.post("/assessment", response_model=ABSAssessmentResult)
async def assess_abs_obligations(data: ABSAssessmentInput):
    return abs_agent.assess(data)
