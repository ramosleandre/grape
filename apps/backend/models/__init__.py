"""
Pydantic models for API requests and responses.
"""

from .requests import (
    QueryRequest,
    GraphEditCommandRequest,
    GraphGenerateRequest,
    GraphImportRequest,
    NodeCreateRequest,
    NodeUpdateRequest,
    LinkCreateRequest,
    SPARQLQueryRequest,
)
from .responses import (
    GraphNode,
    GraphLink,
    ReasoningPath,
    AgentResponse,
    GraphData,
    KnowledgeGraph,
    GraphImportResponse,
    GraphGenerationResponse,
    HealthResponse,
)

__all__ = [
    # Requests
    "QueryRequest",
    "GraphEditCommandRequest",
    "GraphGenerateRequest",
    "GraphImportRequest",
    "NodeCreateRequest",
    "NodeUpdateRequest",
    "LinkCreateRequest",
    "SPARQLQueryRequest",
    # Responses
    "GraphNode",
    "GraphLink",
    "ReasoningPath",
    "AgentResponse",
    "GraphData",
    "KnowledgeGraph",
    "GraphImportResponse",
    "GraphGenerationResponse",
    "HealthResponse",
]
