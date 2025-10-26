"""
Multi-hop Path Explorer Pipeline
Find paths between concepts using N-hop traversal.
"""

from typing import List, Dict, Any, Optional
from pipelines.sparql_query_executor import SPARQLExecutor
from core.config import settings
import logging

logger = logging.getLogger(__name__)


class MultiHopPathExplorer:
    """Explore multi-hop paths between concepts."""

    def __init__(self, endpoint: Optional[str] = None):
        self.executor = SPARQLExecutor(endpoint)

    async def find_paths(
        self,
        source_uri: str,
        target_uri: str,
        max_hops: int = 3,
        max_paths: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Find paths between source and target concepts.

        Args:
            source_uri: Starting concept URI
            target_uri: Target concept URI
            max_hops: Maximum path length
            max_paths: Maximum number of paths to return

        Returns:
            List of paths with nodes and links
        """
        paths = []

        for hops in range(1, max_hops + 1):
            hop_paths = await self._find_paths_n_hops(
                source_uri, target_uri, hops, max_paths - len(paths)
            )
            paths.extend(hop_paths)
            if len(paths) >= max_paths:
                break

        return paths[:max_paths]

    async def _find_paths_n_hops(
        self, source: str, target: str, hops: int, limit: int
    ) -> List[Dict[str, Any]]:
        """Find paths with exactly N hops using property paths."""

        # Build property path pattern
        path_pattern = " / ".join(["?p" + str(i) for i in range(hops)])

        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT * WHERE {{
            <{source}> {path_pattern} <{target}> .
        }}
        LIMIT {limit}
        """

        try:
            results = await self.executor.execute(query)

            paths = []
            for result in results:
                # Extract intermediate nodes and properties
                nodes = [source]
                links = []

                # Parse path from result bindings
                for i in range(hops):
                    prop_key = f"p{i}"
                    if prop_key in result:
                        links.append({
                            "relation": result[prop_key],
                            "label": result[prop_key].split("/")[-1]
                        })

                nodes.append(target)

                paths.append({
                    "length": hops,
                    "nodes": nodes,
                    "links": links,
                    "source": source,
                    "target": target,
                })

            return paths

        except Exception as e:
            logger.warning(f"Path search failed for {hops} hops: {e}")
            # Fallback to iterative exploration
            return await self._find_paths_iterative(source, target, hops, limit)

    async def _find_paths_iterative(
        self, source: str, target: str, max_hops: int, limit: int
    ) -> List[Dict[str, Any]]:
        """Fallback iterative path finding."""
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?intermediate ?prop1 ?prop2 WHERE {{
            <{source}> ?prop1 ?intermediate .
            ?intermediate ?prop2 <{target}> .
        }}
        LIMIT {limit}
        """

        try:
            results = await self.executor.execute(query)

            paths = []
            for r in results:
                paths.append({
                    "length": 2,
                    "nodes": [source, r["intermediate"], target],
                    "links": [
                        {
                            "relation": r["prop1"],
                            "label": r["prop1"].split("/")[-1]
                        },
                        {
                            "relation": r["prop2"],
                            "label": r["prop2"].split("/")[-1]
                        }
                    ],
                    "source": source,
                    "target": target,
                })

            return paths

        except Exception as e:
            logger.error(f"Iterative path search failed: {e}")
            return []

    async def explore_neighborhood_paths(
        self, concept_uri: str, max_hops: int = 2, limit: int = 50
    ) -> Dict[str, Any]:
        """
        Explore all paths from a concept up to N hops.

        Returns:
            Graph structure with reachable nodes and paths
        """
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?node ?property ?label WHERE {{
            <{concept_uri}> (rdfs:subClassOf|^rdfs:subClassOf|?p){{1,{max_hops}}} ?node .
            OPTIONAL {{ ?node rdfs:label ?label }}
            OPTIONAL {{ <{concept_uri}> ?property ?node }}
        }}
        LIMIT {limit}
        """

        try:
            results = await self.executor.execute(query)

            nodes = set()
            links = []

            for r in results:
                node_uri = r["node"]
                nodes.add((node_uri, r.get("label", node_uri.split("/")[-1])))

                if r.get("property"):
                    links.append({
                        "source": concept_uri,
                        "target": node_uri,
                        "relation": r["property"],
                    })

            return {
                "center": concept_uri,
                "nodes": [{"id": uri, "label": lbl} for uri, lbl in nodes],
                "links": links,
                "max_hops": max_hops,
            }

        except Exception as e:
            logger.error(f"Neighborhood exploration failed: {e}")
            return {"center": concept_uri, "nodes": [], "links": []}
