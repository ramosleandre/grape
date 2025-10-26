"""
Test Wikidata SPARQL query directly
"""
import asyncio
from pipelines.sparql_query_executor import SPARQLExecutor

WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"

async def test_simple_query():
    """Test a very simple Wikidata query."""
    executor = SPARQLExecutor(endpoint=WIKIDATA_ENDPOINT)
    
    # Simple query to get statements about Paris (Q90)
    query = """
    SELECT ?property ?value WHERE {
        <http://www.wikidata.org/entity/Q90> ?property ?value .
    }
    LIMIT 10
    """
    
    print("Testing simple query...")
    try:
        results = await executor.execute(query)
        print(f"✓ Got {len(results)} results")
        if results:
            print(f"Sample result: {results[0]}")
    except Exception as e:
        print(f"✗ Error: {e}")


async def test_wdt_query():
    """Test query with wdt: prefix."""
    executor = SPARQLExecutor(endpoint=WIKIDATA_ENDPOINT)
    
    query = """
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?property ?value ?valueLabel WHERE {
        wd:Q90 ?property ?value .
        FILTER(STRSTARTS(STR(?property), "http://www.wikidata.org/prop/direct/"))
        FILTER(STRSTARTS(STR(?value), "http://www.wikidata.org/entity/Q"))
        
        OPTIONAL { ?value rdfs:label ?valueLabel . FILTER(LANG(?valueLabel) = "en") }
    }
    LIMIT 10
    """
    
    print("\nTesting wdt: query with labels...")
    try:
        results = await executor.execute(query)
        print(f"✓ Got {len(results)} results")
        if results:
            print(f"Sample result: {results[0]}")
            for r in results[:3]:
                print(f"  - {r}")
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_simple_query())
    asyncio.run(test_wdt_query())
