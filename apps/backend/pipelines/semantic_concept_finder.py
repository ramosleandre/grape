"""
Semantic Concept Finder Pipeline
Find concepts using gen2kgbot's embedding-based similarity search.

This pipeline automatically embeds the user's question and compares it with
pre-computed embeddings of KG concepts using LangChain's similarity_search.

Uses:
- gen2kgbot/app/utils/config_manager.py - get_class_context_vector_db()
- gen2kgbot embedding models (nomic-embed-text via Ollama)
- LangChain VectorStore.similarity_search() - auto-embeds query and compares
"""

from typing import List, Dict, Any, Optional
from pipelines.sparql_query_executor import SPARQLExecutor
from core.config import settings
import logging
import sys
from pathlib import Path

# Add gen2kgbot to path
gen2kgbot_path = Path(__file__).parent.parent / "gen2kgbot"
if str(gen2kgbot_path) not in sys.path:
    sys.path.insert(0, str(gen2kgbot_path))

logger = logging.getLogger(__name__)


class SemanticConceptFinder:
    """
    Find matching concepts using gen2kgbot embeddings.

    Automatically embeds user query and finds semantically similar KG concepts.
    """

    def __init__(
        self,
        endpoint: Optional[str] = None,
        kg_name: Optional[str] = None,
        scenario_id: str = "scenario_3"
    ):
        self.executor = SPARQLExecutor(endpoint)
        self.kg_name = kg_name or settings.kg_short_name
        self.scenario_id = scenario_id
        self.vector_db = None

    def _init_vector_db(self):
        """Lazy init of gen2kgbot vector DB."""
        if self.vector_db is None:
            try:
                import app.utils.config_manager as config
                self.vector_db = config.get_class_context_vector_db(self.scenario_id)
                logger.info(f"Loaded gen2kgbot vector DB for {self.scenario_id}")
            except Exception as e:
                logger.warning(f"Could not load gen2kgbot vector DB: {e}")
                self.vector_db = None

    async def find(
        self,
        query_text: str,
        limit: int = 10,
        min_similarity: float = 0.5,
    ) -> List[Dict[str, Any]]:
        """
        Find concepts matching the query using embeddings.

        Args:
            query_text: Natural language query
            limit: Max number of concepts
            min_similarity: Minimum similarity threshold

        Returns:
            List of matched concepts
        """
        # Try gen2kgbot vector search first
        concepts = await self._semantic_search(query_text, limit)

        if not concepts:
            # Fallback to keyword search
            concepts = await self._keyword_search(query_text, limit)

        return concepts[:limit]

    async def _semantic_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """
        Use gen2kgbot vector DB for semantic search.

        LangChain automatically:
        1. Embeds the query using the configured embedding model (nomic-embed-text)
        2. Compares with pre-computed KG concept embeddings
        3. Returns top-k most similar concepts
        """
        self._init_vector_db()

        if not self.vector_db:
            return []

        try:
            # LangChain automatically embeds 'query' and finds similar concepts
            docs = self.vector_db.similarity_search(query, k=limit)

            concepts = []
            for doc in docs:
                # Parse doc format: "(uri, label, description)"
                content = doc.page_content
                metadata = doc.metadata

                concepts.append({
                    "uri": metadata.get("uri", ""),
                    "label": metadata.get("label", ""),
                    "description": content,
                    "score": 1.0,
                })

            return concepts

        except Exception as e:
            logger.warning(f"Semantic search failed: {e}")
            return []

    async def _keyword_search(self, term: str, limit: int) -> List[Dict[str, Any]]:
        """Fallback keyword search via SPARQL."""
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

        SELECT DISTINCT ?concept ?label WHERE {{
            {{
                ?concept rdfs:label ?label .
                FILTER(CONTAINS(LCASE(?label), "{term.lower()}"))
            }}
            UNION
            {{
                ?concept skos:prefLabel ?label .
                FILTER(CONTAINS(LCASE(?label), "{term.lower()}"))
            }}
        }}
        LIMIT {limit}
        """

        try:
            results = await self.executor.execute(query)
            return [
                {
                    "uri": r["concept"],
                    "label": r.get("label", ""),
                    "score": 0.5,
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"Keyword search failed: {e}")
            return []
