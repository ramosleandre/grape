"""
Test Multi-hop Path Explorer Pipeline
Finds paths between concepts in DBpedia.
"""

import pytest
from pipelines.multi_hop_path_explorer import MultiHopPathExplorer


DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"


@pytest.mark.asyncio
async def test_find_paths_cities():
    """Test finding paths between Paris and France."""
    explorer = MultiHopPathExplorer(endpoint=DBPEDIA_ENDPOINT)

    paris = "http://dbpedia.org/resource/Paris"
    france = "http://dbpedia.org/resource/France"

    paths = await explorer.find_paths(paris, france, max_hops=2, max_paths=5)

    print(f"✓ Found {len(paths)} paths from Paris to France")
    if paths:
        print(f"  Shortest path: {paths[0].get('length', 0)} hops")


@pytest.mark.asyncio
async def test_explore_neighborhood_paris():
    """Test exploring neighborhood from Paris."""
    explorer = MultiHopPathExplorer(endpoint=DBPEDIA_ENDPOINT)

    paris = "http://dbpedia.org/resource/Paris"

    result = await explorer.explore_neighborhood_paths(paris, max_hops=2, limit=20)

    assert "nodes" in result
    assert "links" in result
    assert result["center"] == paris

    print(f"✓ Explored Paris neighborhood: {len(result['nodes'])} reachable nodes")


@pytest.mark.asyncio
async def test_find_paths_no_connection():
    """Test when no path exists (or very far)."""
    explorer = MultiHopPathExplorer(endpoint=DBPEDIA_ENDPOINT)

    # Unlikely to find short path
    source = "http://dbpedia.org/resource/Paris"
    target = "http://dbpedia.org/resource/Tokyo"

    paths = await explorer.find_paths(source, target, max_hops=1, max_paths=3)

    print(f"✓ Paris to Tokyo (1-hop): {len(paths)} paths found")


if __name__ == "__main__":
    import asyncio

    print("\n=== Testing Multi-hop Path Explorer ===\n")

    print("1. Finding paths between Paris and France...")
    asyncio.run(test_find_paths_cities())

    print("\n2. Exploring Paris neighborhood...")
    asyncio.run(test_explore_neighborhood_paris())

    print("\n3. Testing distant concepts...")
    asyncio.run(test_find_paths_no_connection())

    print("\n✅ All tests passed!\n")
