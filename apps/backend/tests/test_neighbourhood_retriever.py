"""
Test Neighbourhood Retriever Pipeline
Gets 1-hop neighbors of DBpedia concepts.
"""

import pytest
from pipelines.neighbourhood_retriever import NeighbourhoodRetriever


DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"


@pytest.mark.asyncio
async def test_retrieve_paris_neighbors():
    """Test retrieving neighbors of Paris."""
    retriever = NeighbourhoodRetriever(endpoint=DBPEDIA_ENDPOINT)

    paris_uri = "http://dbpedia.org/resource/Paris"

    result = await retriever.retrieve(paris_uri, max_neighbors=20)

    assert "nodes" in result
    assert "links" in result
    assert result["center_node"] == paris_uri
    assert result["total_neighbors"] > 0

    print(f"✓ Paris has {result['total_neighbors']} neighbors")
    print(f"  Sample nodes: {[n['label'][:30] for n in result['nodes'][:3]]}")
    print(f"  Sample links: {[l['label'][:30] for l in result['links'][:3]]}")


@pytest.mark.asyncio
async def test_retrieve_only_outgoing():
    """Test retrieving only outgoing relationships."""
    retriever = NeighbourhoodRetriever(endpoint=DBPEDIA_ENDPOINT)

    paris_uri = "http://dbpedia.org/resource/Paris"

    result = await retriever.retrieve(
        paris_uri,
        max_neighbors=10,
        include_incoming=False,
        include_outgoing=True
    )

    assert len(result["nodes"]) > 0
    print(f"✓ Outgoing only: {len(result['nodes'])} nodes")


@pytest.mark.asyncio
async def test_retrieve_protein():
    """Test with UniProt protein data."""
    retriever = NeighbourhoodRetriever(endpoint="https://sparql.uniprot.org/sparql")

    # Example protein URI
    protein_uri = "http://purl.uniprot.org/uniprot/P12345"

    result = await retriever.retrieve(protein_uri, max_neighbors=10)

    print(f"✓ Protein neighbors: {result['total_neighbors']}")


if __name__ == "__main__":
    import asyncio

    print("\n=== Testing Neighbourhood Retriever ===\n")

    print("1. Getting Paris neighbors...")
    asyncio.run(test_retrieve_paris_neighbors())

    print("\n2. Testing outgoing only...")
    asyncio.run(test_retrieve_only_outgoing())

    print("\n3. Testing with protein data...")
    asyncio.run(test_retrieve_protein())

    print("\n✅ All tests passed!\n")
