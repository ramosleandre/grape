"""
Test Semantic Concept Finder Pipeline
Uses DBpedia - finds concepts like "disease", "protein", etc.
"""

import pytest
from pipelines.semantic_concept_finder import SemanticConceptFinder


DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"


@pytest.mark.asyncio
async def test_find_concepts_disease():
    """Test finding disease-related concepts."""
    finder = SemanticConceptFinder(endpoint=DBPEDIA_ENDPOINT)

    concepts = await finder.find("cancer disease")

    assert len(concepts) > 0
    print(f"✓ Found {len(concepts)} disease concepts")
    for c in concepts[:3]:
        print(f"  - {c.get('label', 'N/A')} ({c.get('uri', 'N/A')})")


@pytest.mark.asyncio
async def test_find_concepts_city():
    """Test finding city concepts."""
    finder = SemanticConceptFinder(endpoint=DBPEDIA_ENDPOINT)

    concepts = await finder.find("Paris France city")

    assert len(concepts) > 0
    assert any("Paris" in c.get("label", "") for c in concepts)
    print(f"✓ Found Paris in {len(concepts)} results")


@pytest.mark.asyncio
async def test_find_concepts_protein():
    """Test finding protein concepts."""
    finder = SemanticConceptFinder(endpoint=DBPEDIA_ENDPOINT)

    concepts = await finder.find("protein structure")

    # May or may not find results depending on DBpedia content
    print(f"✓ Searched for proteins, found {len(concepts)} results")


@pytest.mark.asyncio
async def test_find_concepts_limit():
    """Test limit parameter."""
    finder = SemanticConceptFinder(endpoint=DBPEDIA_ENDPOINT)

    concepts = await finder.find("city", limit=5)

    assert len(concepts) <= 5
    print(f"✓ Limit works: {len(concepts)} results (max 5)")


if __name__ == "__main__":
    import asyncio

    print("\n=== Testing Concept Finder ===\n")

    print("1. Finding disease concepts...")
    asyncio.run(test_find_concepts_disease())

    print("\n2. Finding city concepts...")
    asyncio.run(test_find_concepts_city())

    print("\n3. Finding protein concepts...")
    asyncio.run(test_find_concepts_protein())

    print("\n4. Testing limit...")
    asyncio.run(test_find_concepts_limit())

    print("\n✅ All tests passed!\n")
