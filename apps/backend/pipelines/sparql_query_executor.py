"""
SPARQL Query Executor Pipeline
Executes SPARQL queries using gen2kgbot's sparql_toolkit.

Uses: gen2kgbot/app/utils/sparql_toolkit.py - run_sparql_query()
"""

from typing import List, Dict, Any, Optional
from core.config import settings
import logging
import sys
from pathlib import Path

# Add gen2kgbot to path
gen2kgbot_path = Path(__file__).parent.parent / "gen2kgbot"
if str(gen2kgbot_path) not in sys.path:
    sys.path.insert(0, str(gen2kgbot_path))

from app.utils.sparql_toolkit import run_sparql_query

logger = logging.getLogger(__name__)


class SPARQLExecutor:
    """Execute SPARQL queries using gen2kgbot."""

    def __init__(self, endpoint: Optional[str] = None):
        self.endpoint = endpoint or settings.kg_sparql_endpoint_url
        if not self.endpoint:
            raise ValueError("SPARQL endpoint URL not configured")

    async def execute(
        self,
        query: str,
        max_retries: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Execute SPARQL query using gen2kgbot's toolkit.

        Args:
            query: SPARQL query string
            max_retries: Max retry attempts

        Returns:
            List of results as dictionaries
        """
        for attempt in range(max_retries):
            try:
                # Use gen2kgbot's run_sparql_query (returns CSV)
                csv_result = run_sparql_query(query, self.endpoint)
                return self._parse_csv_results(csv_result)

            except Exception as e:
                logger.warning(f"Query attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    logger.error(f"Query failed after {max_retries} attempts")
                    raise

        return []

    def _parse_csv_results(self, csv_str: str) -> List[Dict[str, Any]]:
        """Parse CSV SPARQL results into list of dicts."""
        # Remove \r and split by \n
        lines = csv_str.replace("\r", "").strip().split("\n")
        if not lines:
            return []

        headers = [h.strip() for h in lines[0].split(",")]
        results = []

        for line in lines[1:]:
            if line.strip():
                values = [v.strip() for v in line.split(",")]
                row = {headers[i]: values[i] if i < len(values) else ""
                       for i in range(len(headers))}
                results.append(row)

        return results

    async def execute_ask(self, query: str) -> bool:
        """Execute ASK query and return boolean result."""
        try:
            csv_result = run_sparql_query(query, self.endpoint)
            return "true" in csv_result.lower()
        except Exception as e:
            logger.error(f"ASK query failed: {e}")
            return False

    async def execute_update(self, query: str) -> bool:
        """Execute UPDATE query (INSERT/DELETE)."""
        try:
            run_sparql_query(query, self.endpoint)
            return True
        except Exception as e:
            logger.error(f"Update query failed: {e}")
            return False
