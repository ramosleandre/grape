"""
Federated Cross-KG Connector Pipeline
Query across multiple knowledge graphs using federated SPARQL.
"""

from typing import List, Dict, Any, Optional
from pipelines.sparql_query_executor import SPARQLExecutor
from core.config import settings
import logging

logger = logging.getLogger(__name__)


class FederatedCrossKGConnector:
    """Connect and query across multiple knowledge graphs."""

    def __init__(self, primary_endpoint: Optional[str] = None):
        self.primary_endpoint = primary_endpoint or settings.kg_sparql_endpoint_url
        self.executor = SPARQLExecutor(self.primary_endpoint)
        self.endpoints = {}

    def register_endpoint(self, kg_name: str, endpoint_url: str):
        """Register a secondary KG endpoint."""
        self.endpoints[kg_name] = endpoint_url
        logger.info(f"Registered endpoint for {kg_name}: {endpoint_url}")

    async def federated_query(
        self,
        local_pattern: str,
        remote_kg: str,
        remote_pattern: str,
        join_var: str = "?concept",
    ) -> List[Dict[str, Any]]:
        """
        Execute federated query across KGs.

        Args:
            local_pattern: SPARQL pattern for local KG
            remote_kg: Name of remote KG
            remote_pattern: SPARQL pattern for remote KG
            join_var: Variable to join on

        Returns:
            Combined results
        """
        if remote_kg not in self.endpoints:
            raise ValueError(f"Endpoint not registered for {remote_kg}")

        remote_endpoint = self.endpoints[remote_kg]

        # Build federated query
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT * WHERE {{
            # Local pattern
            {local_pattern}

            # Remote pattern via SERVICE
            SERVICE <{remote_endpoint}> {{
                {remote_pattern}
            }}
        }}
        LIMIT 100
        """

        try:
            results = await self.executor.execute(query)
            return results

        except Exception as e:
            logger.error(f"Federated query failed: {e}")
            # Fallback: query each endpoint separately and merge
            return await self._fallback_merge(
                local_pattern, remote_kg, remote_pattern, join_var
            )

    async def _fallback_merge(
        self,
        local_pattern: str,
        remote_kg: str,
        remote_pattern: str,
        join_var: str,
    ) -> List[Dict[str, Any]]:
        """Fallback: query each KG separately and merge results."""
        logger.info("Using fallback merge strategy")

        # Query local KG
        local_query = f"""
        SELECT * WHERE {{
            {local_pattern}
        }}
        LIMIT 100
        """

        local_results = await self.executor.execute(local_query)

        # Query remote KG
        remote_executor = SPARQLExecutor(self.endpoints[remote_kg])
        remote_query = f"""
        SELECT * WHERE {{
            {remote_pattern}
        }}
        LIMIT 100
        """

        remote_results = await remote_executor.execute(remote_query)

        # Merge on join variable
        merged = []
        join_key = join_var.lstrip("?")

        for local in local_results:
            for remote in remote_results:
                if local.get(join_key) == remote.get(join_key):
                    merged.append({**local, **remote})

        return merged

    async def find_alignments(
        self,
        concept_uri: str,
        remote_kg: str,
        alignment_properties: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find aligned concepts in remote KG.

        Args:
            concept_uri: URI in local KG
            remote_kg: Remote KG name
            alignment_properties: Properties to check (e.g., owl:sameAs)

        Returns:
            List of aligned concepts
        """
        if not alignment_properties:
            alignment_properties = [
                "http://www.w3.org/2002/07/owl#sameAs",
                "http://www.w3.org/2004/02/skos/core#exactMatch",
                "http://www.w3.org/2004/02/skos/core#closeMatch",
            ]

        if remote_kg not in self.endpoints:
            raise ValueError(f"Endpoint not registered for {remote_kg}")

        remote_endpoint = self.endpoints[remote_kg]

        alignments = []

        for prop in alignment_properties:
            query = f"""
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

            SELECT ?aligned WHERE {{
                {{
                    <{concept_uri}> <{prop}> ?aligned .
                }}
                UNION
                {{
                    SERVICE <{remote_endpoint}> {{
                        ?aligned <{prop}> <{concept_uri}> .
                    }}
                }}
            }}
            """

            try:
                results = await self.executor.execute(query)
                for r in results:
                    alignments.append({
                        "aligned_uri": r["aligned"],
                        "alignment_type": prop.split("/")[-1],
                        "remote_kg": remote_kg,
                    })
            except Exception as e:
                logger.warning(f"Alignment query failed for {prop}: {e}")

        return alignments

    async def cross_kg_path(
        self,
        source_uri: str,
        target_uri: str,
        intermediate_kg: str,
    ) -> List[Dict[str, Any]]:
        """
        Find path from source to target via intermediate KG.

        Args:
            source_uri: URI in local KG
            target_uri: URI in local or remote KG
            intermediate_kg: Bridge KG name

        Returns:
            Cross-KG path
        """
        # Find alignments in intermediate KG
        alignments = await self.find_alignments(source_uri, intermediate_kg)

        if not alignments:
            logger.info("No alignments found")
            return []

        # For each alignment, try to find path to target
        paths = []

        for alignment in alignments[:5]:  # Limit search
            aligned_uri = alignment["aligned_uri"]

            # Check if aligned concept connects to target
            # This is simplified - full implementation would do multi-hop
            query = f"""
            SELECT ?intermediate WHERE {{
                <{aligned_uri}> ?p1 ?intermediate .
                ?intermediate ?p2 <{target_uri}> .
            }}
            LIMIT 10
            """

            remote_executor = SPARQLExecutor(self.endpoints[intermediate_kg])

            try:
                results = await remote_executor.execute(query)
                for r in results:
                    paths.append({
                        "source": source_uri,
                        "aligned_in_remote": aligned_uri,
                        "intermediate": r["intermediate"],
                        "target": target_uri,
                        "bridge_kg": intermediate_kg,
                    })
            except Exception as e:
                logger.warning(f"Cross-KG path search failed: {e}")

        return paths
