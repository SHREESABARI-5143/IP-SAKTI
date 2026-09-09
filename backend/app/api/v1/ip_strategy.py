from fastapi import APIRouter
from backend.app.schemas.ip_strategy import IPStrategyInput, IPStrategyResult
from backend.app.agents.ip_agent import ip_strategy_agent

router = APIRouter(prefix="/ip", tags=["IP Protection Strategy Matrix"])

@router.post("/assessment", response_model=IPStrategyResult)
async def evaluate_ip_strategy(data: IPStrategyInput):
    return ip_strategy_agent.evaluate(data)
