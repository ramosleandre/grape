"""
Proof & Validation Engine Pipeline
Validate and prove assertions using SPARQL reasoning.
"""

from typing import List, Dict, Any, Optional, Tuple
from pipelines.sparql_query_executor import SPARQLExecutor
from pipelines.ontology_context_builder import OntologyContextBuilder
from core.config import settings
import logging

logger = logging.getLogger(__name__)


class ProofValidationEngine:
    """Validate assertions and generate proof traces."""

    def __init__(self, endpoint: Optional[str] = None):
        self.executor = SPARQLExecutor(endpoint)
        self.ontology_builder = OntologyContextBuilder(endpoint)

    async def validate_assertion(
        self,
        subject_uri: str,
        predicate_uri: str,
        object_uri: str,
    ) -> Dict[str, Any]:
        """
        Validate if an assertion exists in the KG.

        Args:
            subject_uri: Subject URI
            predicate_uri: Predicate URI
            object_uri: Object URI

        Returns:
            Validation result with proof
        """
        # Direct check
        direct_exists = await self._check_direct(subject_uri, predicate_uri, object_uri)

        if direct_exists:
            return {
                "valid": True,
                "proof_type": "direct",
                "steps": [
                    f"Found direct triple: <{subject_uri}> <{predicate_uri}> <{object_uri}>"
                ],
            }

        # Inferred check via reasoning
        inferred = await self._check_inferred(subject_uri, predicate_uri, object_uri)

        if inferred["valid"]:
            return inferred

        return {
            "valid": False,
            "proof_type": "none",
            "steps": ["Assertion not found in knowledge graph"],
        }

    async def _check_direct(
        self, subject: str, predicate: str, obj: str
    ) -> bool:
        """Check if triple exists directly."""
        query = f"""
        ASK {{
            <{subject}> <{predicate}> <{obj}> .
        }}
        """

        return await self.executor.execute_ask(query)

    async def _check_inferred(
        self, subject: str, predicate: str, obj: str
    ) -> Dict[str, Any]:
        """Check via inference (property chains, subclass reasoning)."""
        # Check via subclass reasoning
        subclass_proof = await self._check_subclass_reasoning(subject, predicate, obj)
        if subclass_proof["valid"]:
            return subclass_proof

        # Check via property chains
        chain_proof = await self._check_property_chain(subject, predicate, obj)
        if chain_proof["valid"]:
            return chain_proof

        return {"valid": False, "proof_type": "none", "steps": []}

    async def _check_subclass_reasoning(
        self, subject: str, predicate: str, obj: str
    ) -> Dict[str, Any]:
        """Check via rdfs:subClassOf reasoning."""
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?subclass WHERE {{
            <{subject}> a ?subclass .
            ?subclass rdfs:subClassOf+ <{obj}> .
        }}
        LIMIT 1
        """

        try:
            results = await self.executor.execute(query)

            if results:
                return {
                    "valid": True,
                    "proof_type": "subclass_reasoning",
                    "steps": [
                        f"Subject <{subject}> is instance of {results[0]['subclass']}",
                        f"{results[0]['subclass']} is subclass of <{obj}>",
                        f"Therefore assertion holds via transitivity",
                    ],
                }

        except Exception as e:
            logger.warning(f"Subclass reasoning failed: {e}")

        return {"valid": False}

    async def _check_property_chain(
        self, subject: str, predicate: str, obj: str
    ) -> Dict[str, Any]:
        """Check via property path reasoning."""
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?intermediate WHERE {{
            <{subject}> ?p1 ?intermediate .
            ?intermediate ?p2 <{obj}> .
            FILTER(?p1 = <{predicate}> || ?p2 = <{predicate}>)
        }}
        LIMIT 5
        """

        try:
            results = await self.executor.execute(query)

            if results:
                intermediates = [r["intermediate"] for r in results]
                return {
                    "valid": True,
                    "proof_type": "property_chain",
                    "steps": [
                        f"Path exists from <{subject}> to <{obj}>",
                        f"Via intermediate nodes: {intermediates}",
                    ],
                    "intermediates": intermediates,
                }

        except Exception as e:
            logger.warning(f"Property chain check failed: {e}")

        return {"valid": False}

    async def prove_relationship(
        self, source_uri: str, target_uri: str, max_hops: int = 3
    ) -> Dict[str, Any]:
        """
        Prove if any relationship exists between source and target.

        Returns:
            Proof with all found paths
        """
        paths = []

        # Try direct relationship
        direct_path = await self._find_direct_path(source_uri, target_uri)
        if direct_path:
            paths.append(direct_path)

        # Try multi-hop
        for hops in range(2, max_hops + 1):
            hop_paths = await self._find_n_hop_paths(source_uri, target_uri, hops)
            paths.extend(hop_paths)

        if paths:
            return {
                "relationship_exists": True,
                "proof_type": "path_found",
                "paths": paths,
                "steps": [f"Found {len(paths)} connecting paths"],
            }

        return {
            "relationship_exists": False,
            "proof_type": "none",
            "paths": [],
            "steps": ["No paths found between concepts"],
        }

    async def _find_direct_path(
        self, source: str, target: str
    ) -> Optional[Dict[str, Any]]:
        """Find direct 1-hop path."""
        query = f"""
        SELECT ?property WHERE {{
            {{
                <{source}> ?property <{target}> .
            }}
            UNION
            {{
                <{target}> ?property <{source}> .
            }}
        }}
        LIMIT 1
        """

        try:
            results = await self.executor.execute(query)
            if results:
                return {
                    "length": 1,
                    "properties": [results[0]["property"]],
                    "direction": "forward",
                }
        except Exception as e:
            logger.warning(f"Direct path search failed: {e}")

        return None

    async def _find_n_hop_paths(
        self, source: str, target: str, hops: int
    ) -> List[Dict[str, Any]]:
        """Find paths of length N."""
        if hops == 2:
            query = f"""
            SELECT ?intermediate ?p1 ?p2 WHERE {{
                <{source}> ?p1 ?intermediate .
                ?intermediate ?p2 <{target}> .
            }}
            LIMIT 10
            """
        else:
            # Simplified for longer paths
            return []

        try:
            results = await self.executor.execute(query)
            paths = []

            for r in results:
                paths.append({
                    "length": hops,
                    "intermediate_nodes": [r["intermediate"]],
                    "properties": [r["p1"], r["p2"]],
                })

            return paths

        except Exception as e:
            logger.warning(f"N-hop path search failed: {e}")
            return []
