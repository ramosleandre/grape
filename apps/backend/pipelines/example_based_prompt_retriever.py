"""
Example-Based Prompt Retriever Pipeline
Find similar SPARQL query examples for few-shot learning.
"""

from typing import List, Dict, Any, Optional
from core.config import settings
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class ExampleBasedPromptRetriever:
    """Retrieve similar query examples for few-shot prompting."""

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir or settings.gen2kgbot_data_dir)
        self.examples_cache = {}

    async def retrieve(
        self,
        query_text: str,
        kg_name: Optional[str] = None,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Find similar query examples.

        Args:
            query_text: Natural language query
            kg_name: Knowledge graph name
            limit: Max number of examples

        Returns:
            List of similar examples with SPARQL queries
        """
        kg = kg_name or settings.kg_short_name

        # Load examples for this KG
        examples = await self._load_examples(kg)

        if not examples:
            logger.warning(f"No examples found for KG: {kg}")
            return []

        # Rank by similarity
        ranked = self._rank_examples(examples, query_text)

        return ranked[:limit]

    async def _load_examples(self, kg_name: str) -> List[Dict[str, Any]]:
        """Load example queries from data directory."""
        if kg_name in self.examples_cache:
            return self.examples_cache[kg_name]

        # Try to load from gen2kgbot data structure
        examples_path = self.data_dir / kg_name / "example_queries"

        examples = []

        if examples_path.exists():
            for example_file in examples_path.glob("*.json"):
                try:
                    with open(example_file, "r") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            examples.extend(data)
                        else:
                            examples.append(data)
                except Exception as e:
                    logger.warning(f"Failed to load {example_file}: {e}")

        # Fallback: create default examples
        if not examples:
            examples = self._get_default_examples()

        self.examples_cache[kg_name] = examples
        return examples

    def _get_default_examples(self) -> List[Dict[str, Any]]:
        """Default SPARQL query examples."""
        return [
            {
                "question": "What are the properties of X?",
                "sparql": """
                    SELECT ?property ?value WHERE {
                        ?concept ?property ?value .
                    }
                """,
                "description": "Get all properties of a concept",
            },
            {
                "question": "What is connected to X?",
                "sparql": """
                    SELECT ?connected WHERE {
                        { ?concept ?p ?connected }
                        UNION
                        { ?connected ?p ?concept }
                    }
                """,
                "description": "Find all connected entities",
            },
            {
                "question": "What are the subclasses of X?",
                "sparql": """
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    SELECT ?subclass WHERE {
                        ?subclass rdfs:subClassOf ?concept .
                    }
                """,
                "description": "Get subclass hierarchy",
            },
        ]

    def _rank_examples(
        self, examples: List[Dict[str, Any]], query: str
    ) -> List[Dict[str, Any]]:
        """Rank examples by similarity to query."""
        query_lower = query.lower()

        scored = []
        for ex in examples:
            score = 0.0
            question = ex.get("question", "").lower()

            # Simple keyword matching
            query_words = set(query_lower.split())
            question_words = set(question.split())
            common_words = query_words & question_words

            if common_words:
                score = len(common_words) / max(len(query_words), len(question_words))

            scored.append({**ex, "similarity_score": score})

        return sorted(scored, key=lambda x: x["similarity_score"], reverse=True)

    async def get_few_shot_prompt(
        self,
        query_text: str,
        kg_name: Optional[str] = None,
        num_examples: int = 3,
    ) -> str:
        """
        Build few-shot prompt with examples.

        Returns:
            Formatted prompt string
        """
        examples = await self.retrieve(query_text, kg_name, num_examples)

        prompt_parts = [
            "Here are some example SPARQL queries:\n",
        ]

        for i, ex in enumerate(examples, 1):
            prompt_parts.append(f"Example {i}:")
            prompt_parts.append(f"Question: {ex.get('question', '')}")
            prompt_parts.append(f"SPARQL:\n{ex.get('sparql', '')}\n")

        prompt_parts.append(f"Now generate SPARQL for this question:")
        prompt_parts.append(f"Question: {query_text}")
        prompt_parts.append("SPARQL:")

        return "\n".join(prompt_parts)
