"""
Graph data endpoint for knowledge graph visualization.
"""

from fastapi import APIRouter, HTTPException, Path, Query
from typing import Dict, Any
from models.responses import GraphNode, GraphLink
from pipelines.sparql_query_executor import SPARQLExecutor
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Graph"])


@router.get("/graph/{graph_id}", response_model=Dict[str, Any])
async def get_graph_data(
    graph_id: str = Path(..., description="Unique identifier of the graph"),
    sparql_endpoint: str = Query(
        None,
        description="Optional SPARQL endpoint URL for querying external KGs like Wikidata",
    ),
):
    """
    Retrieve graph data for visualization.

    Args:
        graph_id: Graph identifier (placeholder for future database integration)
        sparql_endpoint: Optional SPARQL endpoint URL

    Returns:
        Dictionary with 'nodes' and 'links' lists
    """
    try:
        # For MVP: Return placeholder data
        # TODO: Integrate with database to fetch actual graph data using graph_id

        # If SPARQL endpoint provided, we can query it for demo data
        if sparql_endpoint:
            executor = SPARQLExecutor(endpoint=sparql_endpoint)

            # Simple query to get some data (limit to avoid overload)
            query = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?s ?p ?o ?sLabel ?oLabel WHERE {
                ?s ?p ?o .
                FILTER(isURI(?o))
                OPTIONAL { ?s rdfs:label ?sLabel }
                OPTIONAL { ?o rdfs:label ?oLabel }
            }
            LIMIT 50
            """

            results = await executor.execute(query)

            # Convert to nodes and links
            nodes_dict = {}
            links = []

            for i, r in enumerate(results):
                # Add source node
                s_uri = r.get("s", "")
                if s_uri and s_uri not in nodes_dict:
                    nodes_dict[s_uri] = GraphNode(
                        id=s_uri,
                        label=r.get("sLabel", s_uri.split("/")[-1]),
                        properties={},
                    )

                # Add target node
                o_uri = r.get("o", "")
                if o_uri and o_uri not in nodes_dict:
                    nodes_dict[o_uri] = GraphNode(
                        id=o_uri,
                        label=r.get("oLabel", o_uri.split("/")[-1]),
                        properties={},
                    )

                # Add link
                if s_uri and o_uri:
                    links.append(
                        GraphLink(
                            id=f"link-{i}",
                            source=s_uri,
                            target=o_uri,
                            label=r.get("p", "").split("/")[-1],
                            properties={},
                        )
                    )

            return {
                "nodes": [node.model_dump() for node in nodes_dict.values()],
                "links": [link.model_dump() for link in links],
            }

        # Default placeholder response
        placeholder_nodes = [
            GraphNode(
                id="node1",
                label="Sample Node 1",
                properties={"type": "entity"},
            ),
            GraphNode(
                id="node2",
                label="Sample Node 2",
                properties={"type": "entity"},
            ),
            GraphNode(
                id="node3",
                label="Sample Node 3",
                properties={"type": "entity"},
            ),
        ]

        placeholder_links = [
            GraphLink(
                id="link1",
                source="node1",
                target="node2",
                label="relates_to",
                properties={},
            ),
            GraphLink(
                id="link2",
                source="node2",
                target="node3",
                label="connects_to",
                properties={},
            ),
        ]

        return {
            "nodes": [node.model_dump() for node in placeholder_nodes],
            "links": [link.model_dump() for link in placeholder_links],
        }

    except Exception as e:
        logger.error(f"Failed to retrieve graph data: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve graph data: {str(e)}",
        )
