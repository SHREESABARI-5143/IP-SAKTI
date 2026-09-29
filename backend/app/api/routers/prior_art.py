from fastapi import APIRouter
from app.models.schemas import PriorArtSearchRequest, PriorArtSearchResponse, PriorArtMatch
from app.services.vector_service import vector_service

router = APIRouter(prefix="/api/search", tags=["Prior-Art Search"])

@router.post("/prior-art", response_model=PriorArtSearchResponse)
def search_prior_art(req: PriorArtSearchRequest):
    """Search authoritative AFI/API classical formulation dataset for matching ingredients and prior art."""
    result = vector_service.search_prior_art(
        ingredients=req.ingredients,
        free_text=req.free_text or ""
    )

    matches = [PriorArtMatch(**m) for m in result.get("matches", [])]

    return PriorArtSearchResponse(
        matches=matches,
        summary_verdict=result.get("summary_verdict", "Search completed across AFI corpus."),
        recommendation=result.get("recommendation", "Verify against Section 3(p) and NBA guidelines.")
    )

