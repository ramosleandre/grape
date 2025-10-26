#!/usr/bin/env python3
"""Test Wikidata label fetching query."""

import asyncio
from pipelines.sparql_query_executor import SPARQLExecutor

async def test_label_query():
    executor = SPARQLExecutor(endpoint="https://query.wikidata.org/sparql")
    
    # Test with a simple label query
    ids = ["Q142", "Q90", "Q46"]
    values = " ".join([f"wd:{id}" for id in ids])
    
    query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?item ?label WHERE {{
        VALUES ?item {{ {values} }}
        ?item rdfs:label ?label .
        FILTER(LANG(?label) = "en")
    }}
    """
    
    print("Testing label query:")
    print(query)
    print("\n" + "="*80 + "\n")
    
    try:
        results = await executor.execute(query)
        print(f"Success! Got {len(results)} results:")
        for r in results:
            print(f"  {r}")
    except Exception as e:
        print(f"Failed: {e}")
        
        # Try simpler version without VALUES
        print("\nTrying simpler query without VALUES...")
        simple_query = """
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?label WHERE {
            wd:Q90 rdfs:label ?label .
            FILTER(LANG(?label) = "en")
        }
        LIMIT 1
        """
        print(simple_query)
        try:
            results = await executor.execute(simple_query)
            print(f"Simple query success! Got {len(results)} results:")
            for r in results:
                print(f"  {r}")
        except Exception as e2:
            print(f"Simple query also failed: {e2}")

if __name__ == "__main__":
    asyncio.run(test_label_query())
