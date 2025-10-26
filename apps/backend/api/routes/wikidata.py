"""
Wikidata-specific endpoint for URL-based graph retrieval.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from models.responses import GraphNode, GraphLink
from pipelines.sparql_query_executor import SPARQLExecutor
from pipelines.neighbourhood_retriever import NeighbourhoodRetriever
import logging
import re

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Wikidata"])

WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"


class WikidataRequest(BaseModel):
    """Request model for Wikidata visualization."""

    wikidata_url: Optional[str] = None
    entity_id: Optional[str] = None


@router.post("/wikidata/visualize", response_model=Dict[str, Any])
async def visualize_wikidata_entity(request: WikidataRequest):
    """
    Retrieve and visualize a Wikidata entity's neighborhood.

    Args:
        request: Contains either wikidata_url or entity_id

    Returns:
        Dictionary with 'nodes' and 'links' lists for graph visualization
    """
    try:
        # Extract entity ID
        entity_id = request.entity_id

        if not entity_id and request.wikidata_url:
            # Extract entity ID from URL (e.g., Q90 from https://www.wikidata.org/wiki/Q90)
            match = re.search(r"/(Q\d+)", request.wikidata_url)
            if match:
                entity_id = match.group(1)
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid Wikidata URL format. Expected format: https://www.wikidata.org/wiki/Q123",
                )

        if not entity_id:
            raise HTTPException(
                status_code=400,
                detail="Either wikidata_url or entity_id must be provided",
            )

        # Validate entity ID format
        if not re.match(r"^Q\d+$", entity_id):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid entity ID format: {entity_id}. Expected format: Q123",
            )

        # Construct entity URI
        entity_uri = f"http://www.wikidata.org/entity/{entity_id}"

        # Use NeighbourhoodRetriever to get 1-hop neighborhood
        retriever = NeighbourhoodRetriever(endpoint=WIKIDATA_ENDPOINT)

        # Get neighborhood data (limit to 50 neighbors for performance)
        neighborhood = await retriever.retrieve(
            concept_uri=entity_uri,
            max_neighbors=50,
            include_incoming=True,
            include_outgoing=True,
        )

        # Add the center node if not already present
        nodes_dict = {n["id"]: n for n in neighborhood.get("nodes", [])}

        if entity_uri not in nodes_dict:
            # Query for center node label
            center_label = await _get_entity_label(entity_id, WIKIDATA_ENDPOINT)
            nodes_dict[entity_uri] = {
                "id": entity_uri,
                "label": center_label,
                "type": "center",
            }

        # Convert to GraphNode and GraphLink models
        nodes = [
            GraphNode(
                id=node["id"],
                label=node.get("label", node["id"].split("/")[-1]),
                properties={
                    "type": node.get("type", "entity"),
                },
            )
            for node in nodes_dict.values()
        ]

        links = [
            GraphLink(
                id=f"link-{i}",
                source=link["source"],
                target=link["target"],
                label=link.get("label", "related"),
                properties={
                    "relation": link.get("relation", ""),
                },
            )
            for i, link in enumerate(neighborhood.get("links", []))
        ]

        return {
            "nodes": [node.model_dump() for node in nodes],
            "links": [link.model_dump() for link in links],
            "metadata": {
                "entity_id": entity_id,
                "entity_uri": entity_uri,
                "total_neighbors": neighborhood.get("total_neighbors", 0),
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve Wikidata entity: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve Wikidata entity: {str(e)}",
        )


async def _get_entity_label(entity_id: str, endpoint: str) -> str:
    """
    Get the label for a Wikidata entity.

    Args:
        entity_id: Wikidata entity ID (e.g., Q90)
        endpoint: SPARQL endpoint URL

    Returns:
        Entity label or entity_id if not found
    """
    try:
        executor = SPARQLExecutor(endpoint=endpoint)

        query = f"""
        SELECT ?label WHERE {{
            wd:{entity_id} rdfs:label ?label .
            FILTER(LANG(?label) = "en")
        }}
        LIMIT 1
        """

        results = await executor.execute(query)
        if results and len(results) > 0:
            return results[0].get("label", entity_id)

        return entity_id
    except Exception as e:
        logger.warning(f"Failed to get label for {entity_id}: {e}")
        return entity_id
