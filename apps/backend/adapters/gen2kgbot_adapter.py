"""
Gen2KGBot Adapter

This adapter provides a clean interface to interact with the gen2kgbot library.
It bridges the Grape backend with gen2kgbot's scenarios and utilities.

The adapter:
1. Wraps gen2kgbot's scenario execution
2. Translates between Grape's data models and gen2kgbot's formats
3. Manages gen2kgbot configuration and state
4. Provides a simplified API for the MCP pipelines to use

Usage:
------
    from adapters.gen2kgbot_adapter import Gen2KGBotAdapter

    adapter = Gen2KGBotAdapter(kg_endpoint="http://localhost:7200/...")
    result = await adapter.execute_scenario(
        scenario_id="scenario_7",
        question="What treatments are for patients > 50 years old?"
    )
"""

import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add gen2kgbot to Python path
GEN2KGBOT_PATH = Path(__file__).parent.parent / "gen2kgbot"
if str(GEN2KGBOT_PATH) not in sys.path:
    sys.path.insert(0, str(GEN2KGBOT_PATH))

# Import gen2kgbot modules
try:
    from app.utils.config_manager import get_config
    from app.utils.graph_state import OverallState, InputState
    from app.scenarios.scenario_1.scenario_1 import graph as scenario_1_graph
    from app.scenarios.scenario_2.scenario_2 import graph as scenario_2_graph
    from app.scenarios.scenario_3.scenario_3 import graph as scenario_3_graph
    from app.scenarios.scenario_4.scenario_4 import graph as scenario_4_graph
    from app.scenarios.scenario_5.scenario_5 import graph as scenario_5_graph
    from app.scenarios.scenario_6.scenario_6 import graph as scenario_6_graph
    from app.scenarios.scenario_7.scenario_7 import graph as scenario_7_graph

    GEN2KGBOT_AVAILABLE = True
except ImportError as e:
    logging.warning(f"gen2kgbot import failed: {e}. Adapter will work in mock mode.")
    GEN2KGBOT_AVAILABLE = False


logger = logging.getLogger(__name__)


class Gen2KGBotAdapter:
    """
    Adapter to interface with gen2kgbot library.

    This class provides a high-level API to execute gen2kgbot scenarios
    and translate results into Grape's data models.
    """

    # Mapping of scenario IDs to gen2kgbot graph instances
    SCENARIO_GRAPHS = {
        "scenario_1": "scenario_1_graph" if GEN2KGBOT_AVAILABLE else None,
        "scenario_2": "scenario_2_graph" if GEN2KGBOT_AVAILABLE else None,
        "scenario_3": "scenario_3_graph" if GEN2KGBOT_AVAILABLE else None,
        "scenario_4": "scenario_4_graph" if GEN2KGBOT_AVAILABLE else None,
        "scenario_5": "scenario_5_graph" if GEN2KGBOT_AVAILABLE else None,
        "scenario_6": "scenario_6_graph" if GEN2KGBOT_AVAILABLE else None,
        "scenario_7": "scenario_7_graph" if GEN2KGBOT_AVAILABLE else None,
    }

    def __init__(
        self,
        kg_endpoint: Optional[str] = None,
        ontology_endpoint: Optional[str] = None,
        config_path: Optional[str] = None,
    ):
        """
        Initialize the gen2kgbot adapter.

        Args:
            kg_endpoint: SPARQL endpoint URL for the knowledge graph
            ontology_endpoint: SPARQL endpoint URL for ontologies
            config_path: Path to gen2kgbot configuration file
        """
        self.kg_endpoint = kg_endpoint
        self.ontology_endpoint = ontology_endpoint
        self.config_path = config_path
        self.available = GEN2KGBOT_AVAILABLE

        if not self.available:
            logger.warning("gen2kgbot is not available. Adapter running in mock mode.")

    async def execute_scenario(
        self,
        scenario_id: str,
        question: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Execute a gen2kgbot scenario.

        Args:
            scenario_id: ID of the scenario to execute (e.g., "scenario_7")
            question: Natural language question to process
            context: Additional context for the scenario

        Returns:
            Dict containing:
                - answer: str - Natural language answer
                - sparql_query: Optional[str] - Generated SPARQL query
                - results: Any - Raw results from SPARQL execution
                - reasoning_steps: List[str] - Steps taken during reasoning
        """
        if not self.available:
            return self._mock_execution(scenario_id, question)

        logger.info(f"Executing {scenario_id} with question: {question}")

        try:
            # Get the appropriate scenario graph
            graph = self._get_scenario_graph(scenario_id)

            # Prepare input state
            input_state = InputState(initial_question=question)

            # Execute the graph
            result = await graph.ainvoke(input_state)

            # Extract and format results
            return self._format_result(result, scenario_id)

        except Exception as e:
            logger.error(f"Error executing {scenario_id}: {e}", exc_info=True)
            raise

    def _get_scenario_graph(self, scenario_id: str):
        """Get the LangGraph instance for a specific scenario."""
        if scenario_id == "scenario_1":
            return scenario_1_graph
        elif scenario_id == "scenario_2":
            return scenario_2_graph
        elif scenario_id == "scenario_3":
            return scenario_3_graph
        elif scenario_id == "scenario_4":
            return scenario_4_graph
        elif scenario_id == "scenario_5":
            return scenario_5_graph
        elif scenario_id == "scenario_6":
            return scenario_6_graph
        elif scenario_id == "scenario_7":
            return scenario_7_graph
        else:
            raise ValueError(f"Unknown scenario: {scenario_id}")

    def _format_result(self, result: OverallState, scenario_id: str) -> Dict[str, Any]:
        """
        Format gen2kgbot result into Grape's expected format.

        Args:
            result: OverallState from gen2kgbot execution
            scenario_id: ID of the executed scenario

        Returns:
            Formatted result dictionary
        """
        # Extract relevant information from the state
        messages = result.get("messages", [])
        answer = messages[-1].content if messages else "No answer generated."

        return {
            "answer": answer,
            "sparql_query": result.get("generated_query"),
            "results": result.get("query_results"),
            "reasoning_steps": self._extract_reasoning_steps(result),
            "scenario_used": scenario_id,
            "state": result,  # Include full state for debugging
        }

    def _extract_reasoning_steps(self, state: OverallState) -> List[str]:
        """
        Extract human-readable reasoning steps from the execution state.

        This analyzes the state to produce a narrative of what the agent did.
        """
        steps = []

        # TODO: Implement proper reasoning extraction based on state
        # For now, return placeholder steps
        if state.get("matched_classes"):
            steps.append(f"Matched classes: {state['matched_classes']}")

        if state.get("generated_query"):
            steps.append("Generated SPARQL query")

        if state.get("query_results"):
            steps.append("Executed query and retrieved results")

        return steps if steps else ["Processed question and generated answer"]

    def _mock_execution(self, scenario_id: str, question: str) -> Dict[str, Any]:
        """
        Mock execution when gen2kgbot is not available.

        This is useful for testing and development without full gen2kgbot setup.
        """
        logger.warning(f"Mock execution of {scenario_id}")

        return {
            "answer": f"[MOCK] This is a mock answer for: {question}",
            "sparql_query": "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10",
            "results": [],
            "reasoning_steps": [
                "Mock: Identified concept in question",
                "Mock: Retrieved related entities",
                "Mock: Generated response",
            ],
            "scenario_used": scenario_id,
        }

    def get_available_scenarios(self) -> List[str]:
        """Get list of available gen2kgbot scenarios."""
        return list(self.SCENARIO_GRAPHS.keys())

    def is_available(self) -> bool:
        """Check if gen2kgbot is properly loaded and available."""
        return self.available
