"""
Test Ontology Context Builder Pipeline
Extracts ontology information from DBpedia.
"""

import pytest
from pipelines.ontology_context_builder import OntologyContextBuilder


DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"


@pytest.mark.asyncio
async def test_build_context_city():
    """Test building context for City class."""
    builder = OntologyContextBuilder(endpoint=DBPEDIA_ENDPOINT)

    city_class = "http://dbpedia.org/ontology/City"

    context = await builder.build(city_class)

    assert "concept" in context
    assert "hierarchy" in context
    assert "properties" in context

    print(f"✓ City ontology context:")
    print(f"  Superclasses: {len(context['hierarchy'].get('superclasses', []))}")
    print(f"  Subclasses: {len(context['hierarchy'].get('subclasses', []))}")
    print(f"  Properties: {len(context['properties'])}")


@pytest.mark.asyncio
async def test_build_schema_summary():
    """Test getting schema summary."""
    builder = OntologyContextBuilder(endpoint=DBPEDIA_ENDPOINT)

    summary = await builder.build_schema_summary(limit=10)

    assert "classes" in summary

    print(f"✓ Schema summary: {len(summary['classes'])} main classes")
    for cls in summary['classes'][:3]:
        print(f"  - {cls.get('label', 'N/A')}: {cls.get('instance_count', 0)} instances")


@pytest.mark.asyncio
async def test_build_context_protein():
    """Test with UniProt ontology."""
    builder = OntologyContextBuilder(endpoint="https://sparql.uniprot.org/sparql")

    # UniProt Protein class
    protein_class = "http://purl.uniprot.org/core/Protein"

    context = await builder.build(protein_class, include_properties=True)

    print(f"✓ Protein ontology context: {len(context.get('properties', []))} properties")


if __name__ == "__main__":
    import asyncio

    print("\n=== Testing Ontology Context Builder ===\n")

    print("1. Building City class context...")
    asyncio.run(test_build_context_city())

    print("\n2. Getting schema summary...")
    asyncio.run(test_build_schema_summary())

    print("\n3. Testing with UniProt...")
    asyncio.run(test_build_context_protein())

    print("\n✅ All tests passed!\n")
