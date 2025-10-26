"""
Test Proof & Validation Engine Pipeline
Tests assertion validation on DBpedia.
"""

import pytest
from pipelines.proof_validation_engine import ProofValidationEngine


DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"


@pytest.mark.asyncio
async def test_validate_assertion_true():
    """Test validating a true assertion."""
    engine = ProofValidationEngine(endpoint=DBPEDIA_ENDPOINT)

    # Paris is a City (should be true)
    result = await engine.validate_assertion(
        "http://dbpedia.org/resource/Paris",
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
        "http://dbpedia.org/ontology/City"
    )

    assert result["valid"] is True
    print(f"✓ Paris is a City: VALID")
    print(f"  Proof type: {result.get('proof_type')}")
    print(f"  Steps: {result.get('steps', [])[:2]}")


@pytest.mark.asyncio
async def test_validate_assertion_false():
    """Test validating a false assertion."""
    engine = ProofValidationEngine(endpoint=DBPEDIA_ENDPOINT)

    # Paris is NOT a Planet (should be false)
    result = await engine.validate_assertion(
        "http://dbpedia.org/resource/Paris",
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
        "http://dbpedia.org/ontology/Planet"
    )

    assert result["valid"] is False
    print(f"✓ Paris is a Planet: INVALID (as expected)")


@pytest.mark.asyncio
async def test_prove_relationship():
    """Test proving relationship exists."""
    engine = ProofValidationEngine(endpoint=DBPEDIA_ENDPOINT)

    paris = "http://dbpedia.org/resource/Paris"
    france = "http://dbpedia.org/resource/France"

    result = await engine.prove_relationship(paris, france, max_hops=2)

    print(f"✓ Paris-France relationship: {result['relationship_exists']}")
    if result["paths"]:
        print(f"  Found {len(result['paths'])} paths")


if __name__ == "__main__":
    import asyncio

    print("\n=== Testing Proof & Validation Engine ===\n")

    print("1. Validating true assertion...")
    asyncio.run(test_validate_assertion_true())

    print("\n2. Validating false assertion...")
    asyncio.run(test_validate_assertion_false())

    print("\n3. Proving relationship...")
    asyncio.run(test_prove_relationship())

    print("\n✅ All tests passed!\n")
