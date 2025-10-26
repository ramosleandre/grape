"""
Reasoning Narrator Pipeline
Transform execution traces into human-readable explanations and reasoning paths.
"""

from typing import List, Dict, Any, Optional
from models.responses import ReasoningPath, GraphNode, GraphLink
import logging

logger = logging.getLogger(__name__)


class ReasoningNarrator:
    """Generate human-readable explanations from reasoning traces."""

    def __init__(self):
        pass

    def build_reasoning_path(
        self,
        nodes: List[Dict[str, Any]],
        links: List[Dict[str, Any]],
        steps: List[str],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ReasoningPath:
        """
        Build ReasoningPath from execution data.

        Args:
            nodes: List of graph nodes
            links: List of graph links
            steps: Execution steps
            metadata: Additional metadata

        Returns:
            ReasoningPath object
        """
        graph_nodes = [
            GraphNode(
                id=n.get("id", n.get("uri", f"node_{i}")),
                label=n.get("label", ""),
                properties=n.get("properties", {}),
            )
            for i, n in enumerate(nodes)
        ]

        graph_links = [
            GraphLink(
                id=l.get("id", f"link_{i}"),
                source=l.get("source", ""),
                target=l.get("target", ""),
                label=l.get("label", l.get("relation", "")),
                properties=l.get("properties", {}),
            )
            for i, l in enumerate(links)
        ]

        return ReasoningPath(
            nodes=graph_nodes,
            links=graph_links,
            steps=steps,
            metadata=metadata or {},
        )

    def narrate_concept_exploration(
        self,
        concept: Dict[str, Any],
        neighbors: Dict[str, Any],
    ) -> ReasoningPath:
        """Narrate concept exploration scenario."""
        steps = [
            f"Identified concept: {concept.get('label', concept.get('uri', ''))}",
            f"Retrieved {neighbors.get('total_neighbors', 0)} direct relationships",
        ]

        # Analyze relationship types
        relation_types = {}
        for link in neighbors.get("links", []):
            rel = link.get("label", "unknown")
            relation_types[rel] = relation_types.get(rel, 0) + 1

        if relation_types:
            top_relations = sorted(
                relation_types.items(), key=lambda x: x[1], reverse=True
            )[:3]
            steps.append(
                f"Main relationship types: {', '.join([f'{r} ({c})' for r, c in top_relations])}"
            )

        return self.build_reasoning_path(
            nodes=neighbors.get("nodes", []),
            links=neighbors.get("links", []),
            steps=steps,
            metadata={"scenario": "concept_exploration", "concept": concept},
        )

    def narrate_path_finding(
        self,
        source: str,
        target: str,
        paths: List[Dict[str, Any]],
    ) -> ReasoningPath:
        """Narrate path finding scenario."""
        steps = [
            f"Searching for paths from {source} to {target}",
            f"Found {len(paths)} connecting paths",
        ]

        if paths:
            shortest = min(paths, key=lambda p: p.get("length", 999))
            steps.append(
                f"Shortest path length: {shortest.get('length', 0)} hops"
            )

            # Describe shortest path
            if "nodes" in shortest:
                path_desc = " -> ".join(
                    [n.get("label", n.get("id", "?"))[:30] for n in shortest["nodes"]]
                )
                steps.append(f"Path: {path_desc}")

        # Collect all nodes and links from paths
        all_nodes = []
        all_links = []

        for path in paths:
            all_nodes.extend(path.get("nodes", []))
            all_links.extend(path.get("links", []))

        return self.build_reasoning_path(
            nodes=all_nodes,
            links=all_links,
            steps=steps,
            metadata={
                "scenario": "path_finding",
                "source": source,
                "target": target,
                "path_count": len(paths),
            },
        )

    def narrate_validation(
        self,
        assertion: str,
        validation_result: Dict[str, Any],
    ) -> ReasoningPath:
        """Narrate validation/proof scenario."""
        steps = [
            f"Validating assertion: {assertion}",
        ]

        if validation_result.get("valid"):
            steps.append(f"✓ Assertion is VALID")
            steps.append(f"Proof type: {validation_result.get('proof_type', 'unknown')}")

            if "steps" in validation_result:
                steps.extend(validation_result["steps"])
        else:
            steps.append("✗ Assertion is INVALID")
            steps.append("No evidence found in knowledge graph")

        return self.build_reasoning_path(
            nodes=[],
            links=[],
            steps=steps,
            metadata={
                "scenario": "validation",
                "assertion": assertion,
                "valid": validation_result.get("valid", False),
            },
        )

    def narrate_federated_query(
        self,
        local_kg: str,
        remote_kgs: List[str],
        results: List[Dict[str, Any]],
    ) -> ReasoningPath:
        """Narrate federated query scenario."""
        steps = [
            f"Querying local KG: {local_kg}",
            f"Federated with remote KGs: {', '.join(remote_kgs)}",
            f"Retrieved {len(results)} cross-KG results",
        ]

        # Extract nodes and links from results
        nodes = []
        links = []

        for result in results:
            if "nodes" in result:
                nodes.extend(result["nodes"])
            if "links" in result:
                links.extend(result["links"])

        return self.build_reasoning_path(
            nodes=nodes,
            links=links,
            steps=steps,
            metadata={
                "scenario": "federated_query",
                "local_kg": local_kg,
                "remote_kgs": remote_kgs,
            },
        )

    def generate_natural_language_summary(
        self,
        reasoning_path: ReasoningPath,
    ) -> str:
        """
        Generate natural language summary from reasoning path.

        Returns:
            Human-readable summary
        """
        summary_parts = []

        # Add scenario context
        scenario = reasoning_path.metadata.get("scenario", "unknown")
        summary_parts.append(f"Scenario: {scenario.replace('_', ' ').title()}")

        # Add key findings
        if reasoning_path.nodes:
            summary_parts.append(f"Found {len(reasoning_path.nodes)} relevant concepts")

        if reasoning_path.links:
            summary_parts.append(f"Identified {len(reasoning_path.links)} relationships")

        # Add step summary
        if reasoning_path.steps:
            summary_parts.append("\nReasoning steps:")
            for i, step in enumerate(reasoning_path.steps[:5], 1):
                summary_parts.append(f"{i}. {step}")

        return "\n".join(summary_parts)

    def extract_key_insights(
        self,
        reasoning_path: ReasoningPath,
    ) -> List[str]:
        """
        Extract key insights from reasoning path.

        Returns:
            List of insights
        """
        insights = []

        # Analyze node types
        node_types = {}
        for node in reasoning_path.nodes:
            node_type = node.type or "unknown"
            node_types[node_type] = node_types.get(node_type, 0) + 1

        if node_types:
            insights.append(
                f"Concept types: {', '.join([f'{t}: {c}' for t, c in node_types.items()])}"
            )

        # Analyze relationship patterns
        relation_freq = {}
        for link in reasoning_path.links:
            rel = link.label or link.relation
            relation_freq[rel] = relation_freq.get(rel, 0) + 1

        if relation_freq:
            top_rel = max(relation_freq.items(), key=lambda x: x[1])
            insights.append(f"Most common relationship: {top_rel[0]} ({top_rel[1]} occurrences)")

        return insights
