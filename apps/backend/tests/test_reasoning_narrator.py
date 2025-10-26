"""
Test Reasoning Narrator Pipeline
Tests explanation generation (no endpoint needed).
"""

import pytest
from pipelines.reasoning_narrator import ReasoningNarrator


def test_build_reasoning_path():
    """Test building reasoning path from data."""
    narrator = ReasoningNarrator()

    nodes = [
        {"id": "node1", "label": "Paris", "type": "City"},
        {"id": "node2", "label": "France", "type": "Country"},
    ]

    links = [
        {"source": "node1", "target": "node2", "relation": "country", "label": "country"}
    ]

    steps = [
        "Identified concept: Paris",
        "Found 1 relationship",
    ]

    path = narrator.build_reasoning_path(nodes, links, steps)

    assert len(path.nodes) == 2
    assert len(path.links) == 1
    assert len(path.steps) == 2

    print("✓ Built reasoning path")
    print(f"  Nodes: {[n.label for n in path.nodes]}")
    print(f"  Links: {[l.label for l in path.links]}")


def test_narrate_concept_exploration():
    """Test narrating concept exploration."""
    narrator = ReasoningNarrator()

    concept = {"uri": "http://example.org/Paris", "label": "Paris"}
    neighbors = {
        "nodes": [{"id": "n1", "label": "France"}],
        "links": [{"source": "paris", "target": "n1", "label": "country"}],
        "total_neighbors": 1,
    }

    path = narrator.narrate_concept_exploration(concept, neighbors)

    assert "Paris" in path.steps[0]
    print("✓ Narrated concept exploration")
    print(f"  Steps: {path.steps}")


def test_narrate_path_finding():
    """Test narrating path finding."""
    narrator = ReasoningNarrator()

    paths = [
        {
            "length": 2,
            "nodes": [
                {"id": "paris", "label": "Paris"},
                {"id": "france", "label": "France"}
            ],
            "links": [{"relation": "country"}]
        }
    ]

    path = narrator.narrate_path_finding("Paris", "France", paths)

    assert "Found 1" in path.steps[1]
    print("✓ Narrated path finding")


def test_generate_summary():
    """Test generating natural language summary."""
    narrator = ReasoningNarrator()

    path = narrator.build_reasoning_path(
        [{"id": "n1", "label": "Node 1"}],
        [{"source": "n1", "target": "n2", "relation": "rel", "label": "rel"}],
        ["Step 1", "Step 2"]
    )

    summary = narrator.generate_natural_language_summary(path)

    assert len(summary) > 0
    assert "Found 1 relevant concepts" in summary

    print("✓ Generated summary:")
    print(summary)


if __name__ == "__main__":
    print("\n=== Testing Reasoning Narrator ===\n")

    print("1. Building reasoning path...")
    test_build_reasoning_path()

    print("\n2. Narrating concept exploration...")
    test_narrate_concept_exploration()

    print("\n3. Narrating path finding...")
    test_narrate_path_finding()

    print("\n4. Generating summary...")
    test_generate_summary()

    print("\n✅ All tests passed!\n")
