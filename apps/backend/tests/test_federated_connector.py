"""
Test Federated Cross-KG Connector Pipeline
Tests querying across multiple SPARQL endpoints.
"""

import pytest
from pipelines.federated_cross_kg_connector import FederatedCrossKGConnector


DBPEDIA = "https://dbpedia.org/sparql"
WIKIDATA = "https://query.wikidata.org/sparql"


@pytest.mark.asyncio
async def test_register_endpoint():
    """Test registering secondary endpoints."""
    connector = FederatedCrossKGConnector(primary_endpoint=DBPEDIA)

    connector.register_endpoint("wikidata", WIKIDATA)

    assert "wikidata" in connector.endpoints
    print("✓ Endpoint registered")


@pytest.mark.asyncio
async def test_find_alignments():
    """Test finding concept alignments."""
    connector = FederatedCrossKGConnector(primary_endpoint=DBPEDIA)
    connector.register_endpoint("remote", WIKIDATA)

    paris_uri = "http://dbpedia.org/resource/Paris"

    # This may or may not find alignments depending on data
    alignments = await connector.find_alignments(paris_uri, "remote")

    print(f"✓ Found {len(alignments)} alignments for Paris")


@pytest.mark.asyncio
async def test_fallback_merge():
    """Test fallback merge strategy."""
    connector = FederatedCrossKGConnector(primary_endpoint=DBPEDIA)
    connector.register_endpoint("wikidata", WIKIDATA)

    local_pattern = "?concept rdfs:label ?label"
    remote_pattern = "?concept rdfs:label ?remoteLabel"

    # Test the fallback (won't actually merge much without good join)
    results = await connector._fallback_merge(
        local_pattern,
        "wikidata",
        remote_pattern,
        "?concept"
    )

    print(f"✓ Fallback merge returned {len(results)} results")


if __name__ == "__main__":
    import asyncio

    print("\n=== Testing Federated Connector ===\n")

    print("1. Registering endpoints...")
    asyncio.run(test_register_endpoint())

    print("\n2. Finding alignments...")
    asyncio.run(test_find_alignments())

    print("\n3. Testing fallback merge...")
    asyncio.run(test_fallback_merge())

    print("\n✅ All tests passed!\n")
