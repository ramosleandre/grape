"""
MCP Tools Router - Exposes all 9 pipelines as HTTP endpoints

Simple wrapper around the pipelines for testing and HTTP access.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# Import all 9 pipelines
from pipelines.sparql_query_executor import SPARQLExecutor
from pipelines.semantic_concept_finder import SemanticConceptFinder
from pipelines.neighbourhood_retriever import NeighbourhoodRetriever
from pipelines.multi_hop_path_explorer import MultiHopPathExplorer
from pipelines.ontology_context_builder import OntologyContextBuilder
from pipelines.example_based_prompt_retriever import ExampleBasedPromptRetriever
from pipelines.federated_cross_kg_connector import FederatedCrossKGConnector
from pipelines.proof_validation_engine import ProofValidationEngine
from pipelines.reasoning_narrator import ReasoningNarrator

router = APIRouter(prefix="/mcp", tags=["MCP Tools"])

# Initialize pipelines (singleton pattern)
_sparql_executor = None
_concept_finder = None
_neighbourhood_retriever = None
_path_explorer = None
_ontology_builder = None
_example_retriever = None
_federated_connector = None
_proof_engine = None
_reasoning_narrator = None


def get_sparql_executor() -> SPARQLExecutor:
    global _sparql_executor
    if _sparql_executor is None:
        _sparql_executor = SPARQLExecutor()
    return _sparql_executor


def get_concept_finder() -> SemanticConceptFinder:
    global _concept_finder
    if _concept_finder is None:
        _concept_finder = SemanticConceptFinder()
    return _concept_finder


def get_neighbourhood_retriever() -> NeighbourhoodRetriever:
    global _neighbourhood_retriever
    if _neighbourhood_retriever is None:
        _neighbourhood_retriever = NeighbourhoodRetriever()
    return _neighbourhood_retriever


def get_path_explorer() -> MultiHopPathExplorer:
    global _path_explorer
    if _path_explorer is None:
        _path_explorer = MultiHopPathExplorer()
    return _path_explorer


def get_ontology_builder() -> OntologyContextBuilder:
    global _ontology_builder
    if _ontology_builder is None:
        _ontology_builder = OntologyContextBuilder()
    return _ontology_builder


def get_example_retriever() -> ExampleBasedPromptRetriever:
    global _example_retriever
    if _example_retriever is None:
        _example_retriever = ExampleBasedPromptRetriever()
    return _example_retriever


def get_federated_connector() -> FederatedCrossKGConnector:
    global _federated_connector
    if _federated_connector is None:
        _federated_connector = FederatedCrossKGConnector()
    return _federated_connector


def get_proof_engine() -> ProofValidationEngine:
    global _proof_engine
    if _proof_engine is None:
        _proof_engine = ProofValidationEngine()
    return _proof_engine


def get_reasoning_narrator() -> ReasoningNarrator:
    global _reasoning_narrator
    if _reasoning_narrator is None:
        _reasoning_narrator = ReasoningNarrator()
    return _reasoning_narrator


# ============================================================================
# Request/Response Models
# ============================================================================


class SPARQLQueryRequest(BaseModel):
    query: str = Field(..., description="SPARQL query string")
    max_retries: int = Field(3, description="Maximum retry attempts")


class ConceptFinderRequest(BaseModel):
    query_text: str = Field(..., description="Natural language query")
    limit: int = Field(10, description="Maximum number of concepts")
    min_similarity: float = Field(0.5, description="Minimum similarity threshold")


class NeighbourhoodRequest(BaseModel):
    concept_uri: str = Field(..., description="URI of the concept")
    max_depth: int = Field(1, description="Maximum hop distance")
    include_literals: bool = Field(True, description="Include literal values")


class PathExplorerRequest(BaseModel):
    source_uri: str = Field(..., description="URI of the source concept")
    target_uri: str = Field(..., description="URI of the target concept")
    max_hops: int = Field(3, description="Maximum path length")
    limit: int = Field(10, description="Maximum number of paths")


class OntologyContextRequest(BaseModel):
    concept_uri: Optional[str] = Field(None, description="URI of specific concept (None for full ontology)")
    include_hierarchy: bool = Field(True, description="Include class hierarchy")
    include_properties: bool = Field(True, description="Include properties")
    include_constraints: bool = Field(True, description="Include domain/range constraints")


class ExampleRetrieverRequest(BaseModel):
    query_text: str = Field(..., description="Natural language question")
    limit: int = Field(5, description="Maximum number of examples")
    use_embeddings: bool = Field(True, description="Use embedding-based search")


class FederatedQueryRequest(BaseModel):
    local_pattern: str = Field(..., description="SPARQL pattern for local KG")
    remote_endpoint_name: str = Field(..., description="Name of registered remote endpoint")
    remote_pattern: str = Field(..., description="SPARQL pattern for remote KG")
    join_variable: Optional[str] = Field(None, description="Variable to join on")


class ValidationRequest(BaseModel):
    subject_uri: str = Field(..., description="URI of the subject")
    predicate_uri: str = Field(..., description="URI of the predicate")
    object_uri: str = Field(..., description="URI of the object")
    include_reasoning: bool = Field(True, description="Use reasoning/inference")


class NarratorRequest(BaseModel):
    nodes: List[Dict[str, Any]] = Field(..., description="List of nodes in the reasoning path")
    links: List[Dict[str, Any]] = Field(..., description="List of edges/relationships")
    steps: Optional[List[str]] = Field(None, description="Optional reasoning step descriptions")


# ============================================================================
# Endpoints
# ============================================================================


@router.post("/sparql", response_model=List[Dict[str, Any]])
async def execute_sparql(request: SPARQLQueryRequest):
    """Execute a SPARQL query against the knowledge graph."""
    try:
        executor = get_sparql_executor()
        results = await executor.execute(request.query, request.max_retries)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/concepts", response_model=List[Dict[str, Any]])
async def find_concepts(request: ConceptFinderRequest):
    """Find concepts semantically similar to the query."""
    try:
        finder = get_concept_finder()
        concepts = await finder.find(
            request.query_text, request.limit, request.min_similarity
        )
        return concepts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/neighbourhood", response_model=Dict[str, Any])
async def retrieve_neighbourhood(request: NeighbourhoodRequest):
    """Retrieve the neighbourhood of a concept."""
    try:
        retriever = get_neighbourhood_retriever()
        result = await retriever.retrieve(
            request.concept_uri, request.max_depth, request.include_literals
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/paths", response_model=List[Dict[str, Any]])
async def find_paths(request: PathExplorerRequest):
    """Find paths between two concepts in the knowledge graph."""
    try:
        explorer = get_path_explorer()
        paths = await explorer.find_paths(
            request.source_uri, request.target_uri, request.max_hops, request.limit
        )
        return paths
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ontology", response_model=Dict[str, Any])
async def build_ontology_context(request: OntologyContextRequest):
    """Build ontology context for a concept or the entire ontology."""
    try:
        builder = get_ontology_builder()
        context = await builder.build(
            request.concept_uri,
            request.include_hierarchy,
            request.include_properties,
            request.include_constraints,
        )
        return context
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/examples", response_model=List[Dict[str, Any]])
async def retrieve_examples(request: ExampleRetrieverRequest):
    """Retrieve similar SPARQL query examples for few-shot learning."""
    try:
        retriever = get_example_retriever()
        examples = await retriever.retrieve(
            request.query_text, request.limit, request.use_embeddings
        )
        return examples
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/federated", response_model=List[Dict[str, Any]])
async def query_federated(request: FederatedQueryRequest):
    """Query across multiple knowledge graphs using SPARQL federation."""
    try:
        connector = get_federated_connector()
        results = await connector.federated_query(
            request.local_pattern,
            request.remote_endpoint_name,
            request.remote_pattern,
            request.join_variable,
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate", response_model=Dict[str, Any])
async def validate_assertion(request: ValidationRequest):
    """Validate if an assertion (triple) exists in the knowledge graph."""
    try:
        engine = get_proof_engine()
        result = await engine.validate_assertion(
            request.subject_uri,
            request.predicate_uri,
            request.object_uri,
            request.include_reasoning,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/narrate", response_model=Dict[str, Any])
async def narrate_reasoning(request: NarratorRequest):
    """Transform execution traces into natural language explanations."""
    try:
        narrator = get_reasoning_narrator()
        narrative = narrator.narrate_path(
            request.nodes, request.links, request.steps
        )
        return narrative
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tools")
async def list_tools():
    """List all available MCP tools."""
    return {
        "total": 9,
        "tools": [
            {
                "name": "execute_sparql",
                "endpoint": "/api/mcp/sparql",
                "description": "Execute SPARQL queries",
                "method": "POST",
            },
            {
                "name": "find_concepts",
                "endpoint": "/api/mcp/concepts",
                "description": "Find concepts using embeddings",
                "method": "POST",
            },
            {
                "name": "retrieve_neighbourhood",
                "endpoint": "/api/mcp/neighbourhood",
                "description": "Get connected nodes",
                "method": "POST",
            },
            {
                "name": "find_paths",
                "endpoint": "/api/mcp/paths",
                "description": "Find paths between concepts",
                "method": "POST",
            },
            {
                "name": "build_ontology_context",
                "endpoint": "/api/mcp/ontology",
                "description": "Build ontology context",
                "method": "POST",
            },
            {
                "name": "retrieve_examples",
                "endpoint": "/api/mcp/examples",
                "description": "Get query examples for few-shot learning",
                "method": "POST",
            },
            {
                "name": "query_federated",
                "endpoint": "/api/mcp/federated",
                "description": "Query across multiple KGs",
                "method": "POST",
            },
            {
                "name": "validate_assertion",
                "endpoint": "/api/mcp/validate",
                "description": "Validate triples with proof",
                "method": "POST",
            },
            {
                "name": "narrate_reasoning",
                "endpoint": "/api/mcp/narrate",
                "description": "Generate explanations",
                "method": "POST",
            },
        ],
    }
