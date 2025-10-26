"""
Test SPARQL Query Executor Pipeline
Uses public DBpedia endpoint - no local setup required!
"""

import pytest
from pipelines.sparql_query_executor import SPARQLExecutor


# Public SPARQL endpoints for testing
PUBLIC_ENDPOINTS = {
    "dbpedia": "https://dbpedia.org/sparql",
    "wikidata": "https://query.wikidata.org/sparql",
    "uniprot": "https://sparql.uniprot.org/sparql",
}


@pytest.mark.asyncio
async def test_sparql_executor_basic():
    """Test basic SELECT query on DBpedia."""
    executor = SPARQLExecutor(endpoint=PUBLIC_ENDPOINTS["dbpedia"])

    query = """
    SELECT ?label WHERE {
        <http://dbpedia.org/resource/Paris> rdfs:label ?label .
        FILTER(LANG(?label) = "en")
    }
    LIMIT 1
    """

    results = await executor.execute(query)

    assert len(results) > 0
    assert "label" in results[0]
    assert "Paris" in results[0]["label"]
    print(f"✓ Found Paris: {results[0]['label']}")


@pytest.mark.asyncio
async def test_sparql_executor_wikidata():
    """Test query on Wikidata."""
    executor = SPARQLExecutor(endpoint=PUBLIC_ENDPOINTS["wikidata"])

    query = """
    SELECT ?item ?itemLabel WHERE {
        ?item wdt:P31 wd:Q5 .  # instance of human
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
    }
    LIMIT 5
    """

    results = await executor.execute(query)

    assert len(results) > 0
    print(f"✓ Found {len(results)} humans from Wikidata")


@pytest.mark.asyncio
async def test_sparql_executor_ask_query():
    """Test ASK query."""
    executor = SPARQLExecutor(endpoint=PUBLIC_ENDPOINTS["dbpedia"])

    query = """
    ASK {
        <http://dbpedia.org/resource/Paris> a <http://dbpedia.org/ontology/City>
    }
    """

    result = await executor.execute_ask(query)

    assert result is True
    print("✓ Paris is a city (ASK query works)")


@pytest.mark.asyncio
async def test_sparql_executor_error_handling():
    """Test error handling with invalid query."""
    executor = SPARQLExecutor(endpoint=PUBLIC_ENDPOINTS["dbpedia"])

    invalid_query = "INVALID SPARQL QUERY"

    with pytest.raises(Exception):
        await executor.execute(invalid_query)

    print("✓ Error handling works")


if __name__ == "__main__":
    # Run tests manually
    import asyncio

    print("\n=== Testing SPARQL Executor ===\n")

    print("1. Testing DBpedia query...")
    asyncio.run(test_sparql_executor_basic())

    print("\n2. Testing Wikidata query...")
    asyncio.run(test_sparql_executor_wikidata())

    print("\n3. Testing ASK query...")
    asyncio.run(test_sparql_executor_ask_query())

    print("\n4. Testing error handling...")
    asyncio.run(test_sparql_executor_error_handling())

    print("\n✅ All tests passed!\n")
