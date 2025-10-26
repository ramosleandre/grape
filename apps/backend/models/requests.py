"""
Request models for Grape Backend API.
These Pydantic models define the structure of incoming API requests.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request model for querying the knowledge graph with natural language."""

    question: str = Field(
        ...,
        description="Natural language question to ask the knowledge graph",
        min_length=1,
        examples=["What treatments are associated with protein X?"],
    )
    context_node_ids: Optional[List[str]] = Field(
        default=None,
        description="Optional list of node IDs to constrain the query context",
    )
    scenario_hint: Optional[str] = Field(
        default=None,
        description="Optional hint to suggest which scenario to use (e.g., 'multi_hop', 'validation')",
    )
    max_hops: Optional[int] = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum number of hops for multi-hop reasoning",
    )


class GraphEditCommandRequest(BaseModel):
    """Request model for AI-assisted graph editing with natural language commands."""

    command: str = Field(
        ...,
        description="Natural language command to edit the graph",
        min_length=1,
        examples=["Delete all nodes related to ontology", "Select nodes before 2020"],
    )


class GraphGenerateRequest(BaseModel):
    """Request model for generating a knowledge graph from a document or URL."""

    url: Optional[str] = Field(
        default=None,
        description="URL of a web page to generate the graph from",
    )
    # Note: PDF files will be handled via multipart/form-data in the endpoint


class NodeCreateRequest(BaseModel):
    """Request model for creating a new node in the graph."""

    label: str = Field(..., description="Label/name of the node")
    properties: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional properties for the node",
    )


class NodeUpdateRequest(BaseModel):
    """Request model for updating an existing node."""

    label: Optional[str] = Field(None, description="New label for the node")
    properties: Optional[Dict[str, Any]] = Field(
        None,
        description="Properties to update (will merge with existing)",
    )


class LinkCreateRequest(BaseModel):
    """Request model for creating a new link between nodes."""

    source: str = Field(..., description="ID of the source node")
    target: str = Field(..., description="ID of the target node")
    label: str = Field(..., description="Label/type of the relationship")
    properties: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional properties for the link",
    )


class SPARQLQueryRequest(BaseModel):
    """Request model for direct SPARQL query execution (advanced users)."""

    query: str = Field(
        ...,
        description="SPARQL query to execute",
        min_length=1,
    )
    timeout: Optional[int] = Field(
        default=30,
        ge=1,
        le=300,
        description="Query timeout in seconds",
    )
