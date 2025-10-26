"""
Test Example-Based Prompt Retriever Pipeline
Tests example query retrieval (uses default examples).
"""

import pytest
from pipelines.example_based_prompt_retriever import ExampleBasedPromptRetriever


@pytest.mark.asyncio
async def test_retrieve_examples():
    """Test retrieving similar examples."""
    retriever = ExampleBasedPromptRetriever()

    examples = await retriever.retrieve("What are the properties of X?", limit=3)

    assert len(examples) <= 3
    assert all("question" in ex for ex in examples)

    print(f"✓ Retrieved {len(examples)} examples")
    for ex in examples:
        print(f"  - {ex.get('question', 'N/A')}")


@pytest.mark.asyncio
async def test_get_few_shot_prompt():
    """Test generating few-shot prompt."""
    retriever = ExampleBasedPromptRetriever()

    prompt = await retriever.get_few_shot_prompt(
        "What proteins interact with TP53?",
        num_examples=2
    )

    assert "Example 1:" in prompt
    assert "SPARQL" in prompt

    print(f"✓ Generated few-shot prompt ({len(prompt)} chars)")
    print(prompt[:200] + "...")


@pytest.mark.asyncio
async def test_retrieve_with_custom_kg():
    """Test with custom KG name (will use defaults)."""
    retriever = ExampleBasedPromptRetriever()

    examples = await retriever.retrieve(
        "What are the treatments?",
        kg_name="biokg",
        limit=5
    )

    # Should return default examples if no custom ones exist
    print(f"✓ Retrieved {len(examples)} examples for custom KG")


if __name__ == "__main__":
    import asyncio

    print("\n=== Testing Example-Based Retriever ===\n")

    print("1. Retrieving similar examples...")
    asyncio.run(test_retrieve_examples())

    print("\n2. Generating few-shot prompt...")
    asyncio.run(test_get_few_shot_prompt())

    print("\n3. Testing with custom KG...")
    asyncio.run(test_retrieve_with_custom_kg())

    print("\n✅ All tests passed!\n")
