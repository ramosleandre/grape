"""
Response models for Grape Backend API.
These Pydantic models define the structure of API responses.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class GraphNode(BaseModel):
    """Represents a node in the knowledge graph."""

    id: str = Field(..., description="Unique identifier of the node")
    label: str = Field(..., description="Label/name of the node")
    properties: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional properties of the node",
    )


class GraphLink(BaseModel):
    """Represents a directed link/edge in the knowledge graph."""

    id: str = Field(..., description="Unique identifier of the link")
    source: str = Field(..., description="ID of the source node")
    target: str = Field(..., description="ID of the target node")
    label: str = Field(..., description="Label/type of the relationship")
    properties: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional properties of the link",
    )


class ReasoningPath(BaseModel):
    """Represents the reasoning path taken by the agent."""

    nodes: List[GraphNode] = Field(
        default_factory=list,
        description="Nodes traversed in the reasoning process",
    )
    links: List[GraphLink] = Field(
        default_factory=list,
        description="Links traversed in the reasoning process",
    )
    steps: Optional[List[str]] = Field(
        default=None,
        description="Human-readable explanation of each reasoning step",
    )


class AgentResponse(BaseModel):
    """Response from the Gentoo KGBot agent."""

    answer: str = Field(..., description="Natural language answer to the user's question")
    reasoning_path: ReasoningPath = Field(
        ...,
        description="Visual representation of the agent's reasoning process",
    )
    scenario_used: str = Field(
        ...,
        description="Name of the scenario that was executed (e.g., 'multi_hop_reasoning')",
    )
    sparql_query: Optional[str] = Field(
        default=None,
        description="Generated SPARQL query (if applicable)",
    )
    confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Confidence score of the answer (0-1)",
    )
    sources: Optional[List[str]] = Field(
        default=None,
        description="List of source node/link IDs that contributed to the answer",
    )


class GraphData(BaseModel):
    """Complete graph data for visualization."""

    nodes: List[GraphNode] = Field(..., description="All nodes in the graph")
    links: List[GraphLink] = Field(..., description="All links in the graph")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata about the graph",
    )


class KnowledgeGraph(BaseModel):
    """Metadata about a knowledge graph project."""

    id: str = Field(..., description="Unique identifier of the knowledge graph")
    name: str = Field(..., description="Human-readable name of the graph")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    node_count: Optional[int] = Field(None, description="Total number of nodes")
    link_count: Optional[int] = Field(None, description="Total number of links")


class GraphImportResponse(BaseModel):
    """Response after importing or generating a graph."""

    graph_id: str = Field(..., description="ID of the newly created graph")
    message: str = Field(..., description="Success message")
    node_count: int = Field(..., description="Number of nodes imported")
    link_count: int = Field(..., description="Number of links imported")


class GraphEditResponse(BaseModel):
    """Response after AI-assisted graph editing."""

    message: str = Field(..., description="Description of the action performed")
    affected_nodes: int = Field(
        default=0,
        description="Number of nodes affected by the operation",
    )
    affected_links: int = Field(
        default=0,
        description="Number of links affected by the operation",
    )


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status (e.g., 'healthy')")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(..., description="Current server timestamp")
    services: Dict[str, str] = Field(
        default_factory=dict,
        description="Status of dependent services (e.g., GraphDB, LLM)",
    )


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional error details",
    )
