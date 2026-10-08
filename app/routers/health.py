from datetime import datetime

from fastapi import APIRouter

from app import __version__
from app.schemas.health import HealthResponse

router = APIRouter(prefix="", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        version=__version__,
        timestamp=datetime.utcnow().isoformat(),
    )
