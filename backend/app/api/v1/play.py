from typing import List, Optional
import json
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.core.database import get_db
from backend.app.models.play import PlayScenario

router = APIRouter(prefix="/play", tags=["Play & Educational Scenarios"])

@router.get("/scenarios")
async def get_play_scenarios(locale: str = "en", db: AsyncSession = Depends(get_db)):
    """
    Returns legally grounded interactive scenarios with verified statutory citations.
    """
    result = await db.execute(
        select(PlayScenario).where(PlayScenario.locale == locale)
    )
    scenarios = result.scalars().all()
    if not scenarios:
        # Fallback to English if localized scenarios are not yet seeded
        result = await db.execute(select(PlayScenario).where(PlayScenario.locale == "en"))
        scenarios = result.scalars().all()

    formatted = []
    for sc in scenarios:
        formatted.append({
            "scenario_id": sc.scenario_id,
            "locale": sc.locale,
            "title": sc.title,
            "description": sc.description,
            "choices": json.loads(sc.choices_json) if sc.choices_json else [],
            "outcomes": json.loads(sc.outcomes_json) if sc.outcomes_json else {},
            "citation_ids": json.loads(sc.citation_ids_json) if sc.citation_ids_json else []
        })

    return formatted
