# 🚀 NEXT STEPS - Implementation Guide for Next Agent

## ⚠️ IMPORTANT: gen2kgbot Git Setup

### Current Issue
The `gen2kgbot/` folder was cloned via SSH, which prevents pushing to your repo.

### Solutions

**Option 1: Remove and re-clone via HTTPS (Recommended)**
```bash
cd apps/backend
rm -rf gen2kgbot
git clone https://github.com/Wimmics/gen2kgbot.git
```

**Option 2: Convert SSH to HTTPS**
```bash
cd apps/backend/gen2kgbot
git remote set-url origin https://github.com/Wimmics/gen2kgbot.git
```

**Option 3: Add as Git Submodule (Best Practice)**
```bash
cd /path/to/grape  # Root of your repo
git submodule add https://github.com/Wimmics/gen2kgbot.git apps/backend/gen2kgbot
git submodule update --init --recursive
```

Then in your `.gitignore` or `.gitmodules`, gen2kgbot will be tracked as a submodule, not part of your main repo.

---

## 🎯 Implementation Priority

### Phase 1: Core Pipelines (HIGHEST PRIORITY)

These 9 pipelines are the **foundation** of everything. Implement them first in `pipelines/`:

#### 1. **SPARQL Query Executor** (`sparql_query_executor.py`)
**Why first**: All other pipelines depend on this to execute queries.

**Functionality**:
- Execute SPARQL queries against GraphDB endpoint
- Handle errors and timeouts
- Retry logic
- Return structured results

**Integration with gen2kgbot**:
- Use `gen2kgbot/app/utils/sparql_toolkit.py` functions
- Wrap SPARQLWrapper calls
- Add caching if needed

**Example**:
```python
from pipelines.sparql_query_executor import SPARQLExecutor

executor = SPARQLExecutor(endpoint="http://...")
results = await executor.execute("SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10")
```

---

#### 2. **Semantic Concept Finder** (`semantic_concept_finder.py`)
**Functionality**:
- Find concepts in KG that match user's question
- Use embeddings for semantic matching
- Return ranked list of concepts

**Integration with gen2kgbot**:
- Use preprocessing embeddings from `gen2kgbot/app/preprocessing/compute_embeddings.py`
- Load class descriptions
- Similarity search

**Dependencies**:
- Needs SPARQL Executor
- Needs vector store (ChromaDB/FAISS)

---

#### 3. **Neighbourhood Retriever** (`neighbourhood_retriever.py`)
**Functionality**:
- Get all direct neighbors of a concept (1-hop)
- Return nodes and links

**Integration with gen2kgbot**:
- Query property paths around a concept
- Parse results into GraphNode/GraphLink models

**Dependencies**:
- SPARQL Executor

---

#### 4. **Multi-hop Path Explorer** (`multi_hop_path_explorer.py`)
**Functionality**:
- Find paths between two concepts (N-hops)
- Use property paths in SPARQL
- Return reasoning chains

**Integration with gen2kgbot**:
- Similar to Scenario 2 in gen2kgbot
- Multi-hop property path queries

**Dependencies**:
- SPARQL Executor
- Neighbourhood Retriever

---

#### 5. **Ontology Context Builder** (`ontology_context_builder.py`)
**Functionality**:
- Retrieve ontology/schema info around concepts
- Get classes, properties, hierarchies
- Format for LLM context

**Integration with gen2kgbot**:
- Use ontology endpoint queries
- Parse class/property descriptions
- Similar to Scenario 3/4 in gen2kgbot

**Dependencies**:
- SPARQL Executor

---

#### 6. **Example-Based Prompt Retriever** (`example_based_prompt_retriever.py`)
**Functionality**:
- Find similar example SPARQL queries
- Use for few-shot prompting
- Rank by similarity to question

**Integration with gen2kgbot**:
- Use example queries from `gen2kgbot/data/{kg}/example_queries/`
- Embedding similarity search
- Similar to Scenario 6 in gen2kgbot

**Dependencies**:
- Vector store for examples

---

#### 7. **Federated Cross-KG Connector** (`federated_cross_kg_connector.py`)
**Functionality**:
- Link concepts across multiple KGs
- Execute federated SPARQL (SERVICE)
- Mapping/alignment detection

**Integration with gen2kgbot**:
- Extend SPARQL Executor with SERVICE support
- Cross-endpoint queries

**Dependencies**:
- SPARQL Executor (enhanced)

---

#### 8. **Proof & Validation Engine** (`proof_validation_engine.py`)
**Functionality**:
- Validate/prove assertions
- Use ASK queries
- Property path reasoning
- Return proof trace

**Integration with gen2kgbot**:
- ASK queries + tracing
- SubClassOf reasoning

**Dependencies**:
- SPARQL Executor
- Ontology Context Builder

---

#### 9. **Reasoning Narrator** (`reasoning_narrator.py`)
**Functionality**:
- Take reasoning steps and format them
- Generate human-readable explanations
- Extract reasoning path for visualization

**Integration with gen2kgbot**:
- Parse state from gen2kgbot execution
- Format into ReasoningPath model

**Dependencies**:
- All other pipelines (consumes their output)

---

## 🎨 Phase 2: Scenarios (AFTER Pipelines)

Once pipelines are done, implement scenarios in `scenarios/`:

### Scenario Structure Template

```python
# scenarios/scenario_1_concept_exploration.py
from pipelines.semantic_concept_finder import SemanticConceptFinder
from pipelines.neighbourhood_retriever import NeighbourhoodRetriever
from pipelines.ontology_context_builder import OntologyContextBuilder
from models.responses import AgentResponse, ReasoningPath

async def execute_scenario_1(question: str, context_node_ids=None):
    """
    Scenario 1: Concept Exploration
    User wants to explore info around a concept.
    """
    # Step 1: Find concept
    finder = SemanticConceptFinder()
    concepts = await finder.find(question)

    # Step 2: Get neighbours
    retriever = NeighbourhoodRetriever()
    neighbours = await retriever.retrieve(concepts[0])

    # Step 3: Build ontology context (optional)
    builder = OntologyContextBuilder()
    context = await builder.build(concepts[0])

    # Step 4: Format response
    return AgentResponse(
        answer=f"Found {len(neighbours)} related entities...",
        reasoning_path=ReasoningPath(...),
        scenario_used="scenario_1_concept_exploration",
    )
```

### Scenarios to Implement

1. **scenario_1_concept_exploration.py** - Neighbourhood exploration
2. **scenario_2_multi_hop_reasoning.py** - Path finding
3. **scenario_3_nl2sparql_adaptive.py** - Complex NL2SPARQL with examples
4. **scenario_4_cross_kg_federation.py** - Cross-KG linking
5. **scenario_5_validation_proof.py** - Proof/validation
6. **scenario_6_explainable_reasoning.py** - Explanation generation
7. **scenario_7_filtered_exploration.py** - Filtered queries
8. **scenario_8_alignment_detection.py** - KG alignment
9. **scenario_9_decision_synthesis.py** - Synthesis & recommendations

---

## 🤖 Phase 3: Agent Orchestrator

Implement `core/agent.py` to choose the right scenario:

```python
# core/agent.py
from scenarios import *
from adapters import Gen2KGBotAdapter

class GrapeAgent:
    """Main orchestrator that selects and executes scenarios."""

    def __init__(self):
        self.gen2kgbot_adapter = Gen2KGBotAdapter()

    async def process_question(self, question: str, hint: str = None):
        """
        Analyze question and route to appropriate scenario.
        """
        # Classify question type
        scenario_id = self._classify_question(question, hint)

        # Execute scenario
        if scenario_id in ["scenario_1", "scenario_2", ...]:
            # Use our new scenarios
            result = await execute_scenario_X(question)
        else:
            # Fallback to gen2kgbot adapter
            result = await self.gen2kgbot_adapter.execute_scenario(
                scenario_id, question
            )

        return result

    def _classify_question(self, question: str, hint: str = None):
        """Use LLM or rules to classify question type."""
        # TODO: Implement classification logic
        pass
```

---

## 📡 Phase 4: API Routes

Implement routes in `api/routes/`:

### `api/routes/query.py`

```python
from fastapi import APIRouter, HTTPException
from models.requests import QueryRequest
from models.responses import AgentResponse
from core.agent import GrapeAgent

router = APIRouter(tags=["Query"])
agent = GrapeAgent()

@router.post("/graph/{graph_id}/query-agent", response_model=AgentResponse)
async def query_agent(graph_id: str, request: QueryRequest):
    """
    Query the knowledge graph with natural language.
    The agent will select the appropriate scenario.
    """
    try:
        result = await agent.process_question(
            question=request.question,
            hint=request.scenario_hint,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### `api/routes/graph.py`

CRUD operations for graph management (optional for hackathon).

---

## 🔌 Integration with gen2kgbot - Key Files to Study

### Essential gen2kgbot files to understand:

1. **`gen2kgbot/app/utils/sparql_toolkit.py`**
   - Core SPARQL execution functions
   - Use these in your SPARQL Executor pipeline

2. **`gen2kgbot/app/preprocessing/compute_embeddings.py`**
   - How embeddings are computed
   - Use in Semantic Concept Finder

3. **`gen2kgbot/app/scenarios/scenario_*/scenario_*.py`**
   - Study how scenarios 1-7 work
   - Adapt their logic for your pipelines

4. **`gen2kgbot/app/utils/graph_state.py`**
   - OverallState, InputState structures
   - The adapter already handles conversion

5. **`gen2kgbot/app/utils/config_manager.py`**
   - Configuration loading
   - You can reuse this in your core/config.py

---

## 🧪 Testing Strategy

Create tests in `tests/`:

```python
# tests/test_pipelines.py
import pytest
from pipelines.sparql_query_executor import SPARQLExecutor

@pytest.mark.asyncio
async def test_sparql_executor():
    executor = SPARQLExecutor(endpoint="http://test-endpoint")
    result = await executor.execute("SELECT * WHERE { ?s ?p ?o } LIMIT 1")
    assert result is not None
```

---

## 📚 Resources for Next Agent

### Documentation to Read
1. gen2kgbot README (already provided)
2. LangGraph docs: https://langchain-ai.github.io/langgraph/
3. SPARQL 1.1 spec: https://www.w3.org/TR/sparql11-query/
4. FastAPI async patterns: https://fastapi.tiangolo.com/async/

### Code Examples
- Check `gen2kgbot/app/scenarios/` for scenario patterns
- Check `gen2kgbot/app/utils/` for utility functions
- Use `adapters/gen2kgbot_adapter.py` as reference for integration

### API Testing
```bash
# Once implementation is done, test with:
curl -X POST "http://localhost:8000/api/graph/test-kg/query-agent" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the treatments for disease X?"}'
```

---

## 🎯 Success Criteria

### Minimum Viable Product (MVP)
- ✅ All 9 pipelines implemented and tested
- ✅ At least 3 scenarios working end-to-end
- ✅ Agent can route questions to scenarios
- ✅ API endpoint `/graph/{id}/query-agent` functional
- ✅ gen2kgbot adapter working

### Stretch Goals
- All 9 scenarios implemented
- MCP server exposing pipelines as tools
- Comprehensive tests
- Reasoning path visualization data

---

## ⚡ Quick Start Commands for Next Agent

```bash
# 1. Fix gen2kgbot git issue (choose one option above)

# 2. Activate venv
cd apps/backend
source .venv/bin/activate

# 3. Start server in one terminal
python main.py

# 4. In another terminal, start implementing
# Create first pipeline:
touch pipelines/sparql_query_executor.py

# 5. Test as you go
python -m pytest tests/
```

---

## 📝 Notes & Tips

1. **Reuse gen2kgbot code**: Don't rewrite everything, wrap and extend
2. **Start simple**: Get SPARQL Executor working first
3. **Test incrementally**: Each pipeline should have tests
4. **Use the adapter**: The gen2kgbot_adapter.py is your friend
5. **Check main.py logs**: Debugging info will appear there
6. **Read the flowchart**: `Flowchart.png` shows the architecture

---

**Current Status**: ✅ Setup complete, ready for implementation
**Next Agent Task**: Implement the 9 MCP pipelines + scenarios
**Estimated Time**: 4-6 hours for full implementation

Good luck! 🚀
