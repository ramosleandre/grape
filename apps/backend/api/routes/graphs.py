"""
Graph management API routes.
Handles knowledge graph import, listing, retrieval, and deletion.
"""

import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from rdflib import Graph as RDFGraph

from core.config import settings
from models import (
    GraphImportResponse,
    KnowledgeGraph,
    ErrorResponse,
)
from repositories.graph_repository import GraphRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/graphs", tags=["Graph Management"])

# Supported RDF formats
RDF_FORMATS = {
    ".ttl": "turtle",
    ".rdf": "xml",
    ".nt": "nt",
    ".jsonld": "json-ld",
    ".n3": "n3",
}


def get_graph_repository() -> GraphRepository:
    """Get graph repository instance."""
    if not settings.kg_sparql_endpoint_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="SPARQL endpoint URL not configured. Please set KG_SPARQL_ENDPOINT_URL environment variable.",
        )
    return GraphRepository(settings.kg_sparql_endpoint_url)


@router.post(
    "/import",
    response_model=GraphImportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Import an RDF knowledge graph",
    description="Upload an RDF file (Turtle, RDF/XML, N-Triples, or JSON-LD) to create a new knowledge graph.",
)
async def import_graph(
    file: UploadFile = File(..., description="RDF file to import"),
    name: str = Form(None, description="Optional name for the graph"),
) -> GraphImportResponse:
    """
    Import a knowledge graph from an RDF file.

    This endpoint:
    1. Accepts an RDF file upload
    2. Parses the file using RDFLib
    3. Generates a unique graph ID
    4. Stores metadata in the metadata named graph
    5. Inserts all triples into a named graph in GraphDB

    Args:
        file: RDF file (.ttl, .rdf, .nt, .jsonld)
        name: Optional name for the graph (defaults to filename)

    Returns:
        GraphImportResponse with graph_id, name, and triple_count

    Raises:
        400: Invalid file format or parse error
        500: Database error
    """
    try:
        # Determine file format from extension
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in RDF_FORMATS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file format: {file_extension}. Supported formats: {', '.join(RDF_FORMATS.keys())}",
            )

        rdf_format = RDF_FORMATS[file_extension]

        # Generate graph name if not provided
        if not name:
            name = Path(file.filename).stem.replace("_", " ").replace("-", " ").title()

        # Read and parse the file
        logger.info(f"Parsing RDF file: {file.filename} (format: {rdf_format})")
        content = await file.read()

        rdf_graph = RDFGraph()
        try:
            rdf_graph.parse(data=content, format=rdf_format)
        except Exception as e:
            logger.error(f"Failed to parse RDF file: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to parse RDF file: {str(e)}",
            )

        triple_count = len(rdf_graph)
        logger.info(f"Successfully parsed {triple_count} triples from {file.filename}")

        if triple_count == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded file contains no RDF triples.",
            )

        # Generate unique graph ID
        graph_id = str(uuid.uuid4())
        created_at = datetime.utcnow()

        # Get repository and insert data
        repo = get_graph_repository()

        # Insert metadata
        logger.info(f"Inserting metadata for graph {graph_id}")
        repo.insert_graph_metadata(graph_id, name, created_at)

        # Insert graph data
        logger.info(f"Inserting {triple_count} triples for graph {graph_id}")
        inserted_count = repo.insert_graph_data(graph_id, rdf_graph)

        logger.info(f"Successfully imported graph {graph_id} with {inserted_count} triples")

        return GraphImportResponse(
            graph_id=graph_id,
            name=name,
            triple_count=inserted_count,
            message=f"Successfully imported {inserted_count} triples",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during graph import: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to import graph: {str(e)}",
        )


@router.get(
    "",
    response_model=List[KnowledgeGraph],
    summary="List all knowledge graphs",
    description="Retrieve a list of all imported knowledge graphs with their metadata.",
)
async def list_graphs() -> List[KnowledgeGraph]:
    """
    List all knowledge graphs in the system.

    Returns:
        List of KnowledgeGraph metadata objects
    """
    try:
        repo = get_graph_repository()
        graphs = repo.list_graphs()

        return [
            KnowledgeGraph(
                id=g["id"],
                name=g["name"],
                created_at=datetime.fromisoformat(g["createdAt"].replace("^^http://www.w3.org/2001/XMLSchema#dateTime", "")),
                updated_at=datetime.fromisoformat(g["updatedAt"].replace("^^http://www.w3.org/2001/XMLSchema#dateTime", "")),
            )
            for g in graphs
        ]
    except Exception as e:
        logger.error(f"Failed to list graphs: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list graphs: {str(e)}",
        )


@router.get(
    "/{graph_id}",
    response_model=KnowledgeGraph,
    summary="Get knowledge graph metadata",
    description="Retrieve metadata for a specific knowledge graph.",
)
async def get_graph(graph_id: str) -> KnowledgeGraph:
    """
    Get metadata for a specific knowledge graph.

    Args:
        graph_id: Unique identifier of the graph

    Returns:
        KnowledgeGraph metadata

    Raises:
        404: Graph not found
    """
    try:
        repo = get_graph_repository()
        metadata = repo.get_graph_metadata(graph_id)

        if not metadata:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Graph with ID {graph_id} not found",
            )

        return KnowledgeGraph(
            id=metadata["id"],
            name=metadata["name"],
            created_at=datetime.fromisoformat(metadata["createdAt"].replace("^^http://www.w3.org/2001/XMLSchema#dateTime", "")),
            updated_at=datetime.fromisoformat(metadata["updatedAt"].replace("^^http://www.w3.org/2001/XMLSchema#dateTime", "")),
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get graph metadata: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get graph metadata: {str(e)}",
        )


@router.delete(
    "/{graph_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a knowledge graph",
    description="Delete a knowledge graph and all its data.",
)
async def delete_graph(graph_id: str):
    """
    Delete a knowledge graph and its metadata.

    Args:
        graph_id: Unique identifier of the graph

    Raises:
        404: Graph not found
        500: Database error
    """
    try:
        repo = get_graph_repository()

        # Check if graph exists
        metadata = repo.get_graph_metadata(graph_id)
        if not metadata:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Graph with ID {graph_id} not found",
            )

        # Delete the graph
        repo.delete_graph(graph_id)
        logger.info(f"Successfully deleted graph {graph_id}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete graph: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete graph: {str(e)}",
        )
