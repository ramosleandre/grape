"""
Neighbourhood Retriever Pipeline
Get all direct connections (1-hop) of a concept in the KG.
"""

from typing import List, Dict, Any, Optional
from pipelines.sparql_query_executor import SPARQLExecutor
from core.config import settings
import logging

logger = logging.getLogger(__name__)


class NeighbourhoodRetriever:
    """Retrieve direct neighbors of a concept."""

    def __init__(self, endpoint: Optional[str] = None):
        self.executor = SPARQLExecutor(endpoint)

    async def retrieve(
        self,
        concept_uri: str,
        max_neighbors: int = 100,
        include_incoming: bool = True,
        include_outgoing: bool = True,
    ) -> Dict[str, Any]:
        """
        Get all 1-hop neighbors of a concept.

        Args:
            concept_uri: URI of the concept
            max_neighbors: Max neighbors to retrieve
            include_incoming: Include incoming edges
            include_outgoing: Include outgoing edges

        Returns:
            Dict with nodes and links
        """
        nodes = []
        links = []

        # Get outgoing relationships
        if include_outgoing:
            outgoing = await self._get_outgoing(concept_uri, max_neighbors)
            nodes.extend(outgoing["nodes"])
            links.extend(outgoing["links"])

        # Get incoming relationships
        if include_incoming:
            incoming = await self._get_incoming(concept_uri, max_neighbors)
            nodes.extend(incoming["nodes"])
            links.extend(incoming["links"])

        # Deduplicate nodes
        unique_nodes = {n["id"]: n for n in nodes}

        return {
            "center_node": concept_uri,
            "nodes": list(unique_nodes.values()),
            "links": links,
            "total_neighbors": len(unique_nodes),
        }

    async def _get_outgoing(
        self, concept_uri: str, limit: int
    ) -> Dict[str, List[Dict]]:
        """Get outgoing relationships."""
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?property ?target ?targetLabel ?propertyLabel WHERE {{
            <{concept_uri}> ?property ?target .
            FILTER(isURI(?target))
            OPTIONAL {{ ?target rdfs:label ?targetLabel }}
            OPTIONAL {{ ?property rdfs:label ?propertyLabel }}
        }}
        LIMIT {limit}
        """

        try:
            results = await self.executor.execute(query)
            nodes = []
            links = []

            for r in results:
                target_uri = r["target"]
                nodes.append(
                    {
                        "id": target_uri,
                        "label": r.get("targetLabel", target_uri.split("/")[-1]),
                        "type": "entity",
                    }
                )
                links.append(
                    {
                        "source": concept_uri,
                        "target": target_uri,
                        "relation": r["property"],
                        "label": r.get("propertyLabel", r["property"].split("/")[-1]),
                    }
                )

            return {"nodes": nodes, "links": links}

        except Exception as e:
            logger.error(f"Failed to get outgoing relationships: {e}")
            return {"nodes": [], "links": []}

    async def _get_incoming(
        self, concept_uri: str, limit: int
    ) -> Dict[str, List[Dict]]:
        """Get incoming relationships."""
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?property ?source ?sourceLabel ?propertyLabel WHERE {{
            ?source ?property <{concept_uri}> .
            FILTER(isURI(?source))
            OPTIONAL {{ ?source rdfs:label ?sourceLabel }}
            OPTIONAL {{ ?property rdfs:label ?propertyLabel }}
        }}
        LIMIT {limit}
        """

        try:
            results = await self.executor.execute(query)
            nodes = []
            links = []

            for r in results:
                source_uri = r["source"]
                nodes.append(
                    {
                        "id": source_uri,
                        "label": r.get("sourceLabel", source_uri.split("/")[-1]),
                        "type": "entity",
                    }
                )
                links.append(
                    {
                        "source": source_uri,
                        "target": concept_uri,
                        "relation": r["property"],
                        "label": r.get("propertyLabel", r["property"].split("/")[-1]),
                    }
                )

            return {"nodes": nodes, "links": links}

        except Exception as e:
            logger.error(f"Failed to get incoming relationships: {e}")
            return {"nodes": [], "links": []}
