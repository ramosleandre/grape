"""
Health check endpoint for monitoring and deployment validation.
"""

from fastapi import APIRouter
from datetime import datetime
from models.responses import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    Returns the status of the API and its dependencies.
    """
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        timestamp=datetime.now(),
        services={
            "api": "operational",
            "graphdb": "not_configured",  # TODO: Add actual health check
            "llm": "not_configured",  # TODO: Add actual health check
        },
    )
