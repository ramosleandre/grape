"""
Test Graph Routes
Tests for graph data and Wikidata visualization endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_graph_data_basic():
    """Test basic graph endpoint with placeholder data."""
    response = client.get("/api/graph/placeholder")

    assert response.status_code == 200
    data = response.json()

    assert "nodes" in data
    assert "links" in data
    assert isinstance(data["nodes"], list)
    assert isinstance(data["links"], list)
    assert len(data["nodes"]) > 0
    assert len(data["links"]) > 0

    # Check node structure
    node = data["nodes"][0]
    assert "id" in node
    assert "label" in node
    assert "properties" in node

    # Check link structure
    link = data["links"][0]
    assert "id" in link
    assert "source" in link
    assert "target" in link
    assert "label" in link

    print(f"✓ Graph endpoint returned {len(data['nodes'])} nodes and {len(data['links'])} links")


@pytest.mark.asyncio
async def test_wikidata_entity_retrieval():
    """Test Wikidata endpoint with Q90 (Paris)."""
    response = client.post("/api/wikidata/visualize", json={"entity_id": "Q90"})

    assert response.status_code == 200
    data = response.json()

    assert "nodes" in data
    assert "links" in data
    assert "metadata" in data

    # Check metadata
    metadata = data["metadata"]
    assert metadata["entity_id"] == "Q90"
    assert "entity_uri" in metadata
    assert "total_neighbors" in metadata

    # Check we got some data
    assert len(data["nodes"]) > 0
    print(f"✓ Wikidata endpoint returned {len(data['nodes'])} nodes for Paris (Q90)")


@pytest.mark.asyncio
async def test_wikidata_url_input():
    """Test Wikidata endpoint with full URL."""
    response = client.post(
        "/api/wikidata/visualize", json={"wikidata_url": "https://www.wikidata.org/wiki/Q90"}
    )

    assert response.status_code == 200
    data = response.json()

    assert "nodes" in data
    assert "links" in data
    assert data["metadata"]["entity_id"] == "Q90"

    print("✓ Wikidata URL input works correctly")


@pytest.mark.asyncio
async def test_wikidata_invalid_entity():
    """Test Wikidata endpoint with invalid entity ID."""
    response = client.post("/api/wikidata/visualize", json={"entity_id": "INVALID"})

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data

    print("✓ Invalid entity ID handling works")


@pytest.mark.asyncio
async def test_wikidata_missing_input():
    """Test Wikidata endpoint with missing input."""
    response = client.post("/api/wikidata/visualize", json={})

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data

    print("✓ Missing input handling works")


@pytest.mark.asyncio
async def test_wikidata_different_entities():
    """Test Wikidata with different entities."""
    entities = [
        ("Q5", "Human"),
        ("Q2", "Earth"),
    ]

    for entity_id, name in entities:
        response = client.post("/api/wikidata/visualize", json={"entity_id": entity_id})

        assert response.status_code == 200
        data = response.json()
        assert len(data["nodes"]) > 0

        print(f"✓ Successfully retrieved data for {name} ({entity_id})")


if __name__ == "__main__":
    # Run tests manually
    import asyncio

    print("\n=== Testing Graph Routes ===\n")

    print("1. Testing basic graph endpoint...")
    test_get_graph_data_basic()

    print("\n2. Testing Wikidata entity retrieval (Q90 - Paris)...")
    asyncio.run(test_wikidata_entity_retrieval())

    print("\n3. Testing Wikidata URL input...")
    asyncio.run(test_wikidata_url_input())

    print("\n4. Testing invalid entity handling...")
    asyncio.run(test_wikidata_invalid_entity())

    print("\n5. Testing missing input handling...")
    asyncio.run(test_wikidata_missing_input())

    print("\n6. Testing different entities...")
    asyncio.run(test_wikidata_different_entities())

    print("\n✅ All tests passed!\n")
