# Pipelines - gen2kgbot Integration

This directory contains 9 reusable pipelines that leverage **gen2kgbot** functions for knowledge graph operations.

## gen2kgbot Functions Used

### 1. **SPARQL Query Executor** (`sparql_query_executor.py`)

**Uses:**
- `gen2kgbot/app/utils/sparql_toolkit.py::run_sparql_query()`
  - Executes SPARQL queries and returns CSV format results
  - Handles RDF graph parsing and query validation
  - Built-in error handling

**What it does:**
- Wraps gen2kgbot's SPARQL execution
- Parses CSV results to Python dicts
- Provides retry logic

---

### 2. **Semantic Concept Finder** (`semantic_concept_finder.py`)

**Uses:**
- `gen2kgbot/app/utils/config_manager.py::get_classes_vector_db()`
  - Accesses pre-computed class embeddings
  - Uses FAISS or Chroma vector stores
- `gen2kgbot/app/preprocessing/compute_embeddings.py`
  - Embedding infrastructure

**What it does:**
- Semantic similarity search using gen2kgbot embeddings
- Falls back to keyword search if embeddings unavailable
- Finds concepts matching natural language queries

---

### 3. **Neighbourhood Retriever** (`neighbourhood_retriever.py`)

**Uses:**
- SPARQL Executor (which uses gen2kgbot)

**What it does:**
- Gets 1-hop neighbors of a concept
- Returns nodes and links for visualization

---

### 4. **Multi-hop Path Explorer** (`multi_hop_path_explorer.py`)

**Uses:**
- SPARQL Executor (which uses gen2kgbot)
- SPARQL property paths for N-hop traversal

**What it does:**
- Finds paths between concepts (up to N hops)
- Uses SPARQL 1.1 property path syntax
- Returns all paths with intermediate nodes

---

### 5. **Ontology Context Builder** (`ontology_context_builder.py`)

**Uses:**
- SPARQL Executor (which uses gen2kgbot)
- Can integrate with `gen2kgbot/app/preprocessing/gen_descriptions.py` logic

**What it does:**
- Extracts ontology information (class hierarchy, properties)
- Provides context for LLM prompts
- Gets domain/range constraints

---

### 6. **Example-Based Retriever** (`example_based_prompt_retriever.py`)

**Uses:**
- `gen2kgbot/data/{kg_name}/example_queries/`
  - Loads pre-defined query examples
- Can use `gen2kgbot/app/utils/config_manager.py::get_queries_vector_db()`
  - For embedding-based example retrieval

**What it does:**
- Finds similar SPARQL query examples
- Builds few-shot prompts for LLMs
- Ranks examples by similarity

---

### 7. **Federated Connector** (`federated_cross_kg_connector.py`)

**Uses:**
- SPARQL Executor (which uses gen2kgbot)
- SPARQL 1.1 SERVICE for federation

**What it does:**
- Queries across multiple knowledge graphs
- Finds alignments (owl:sameAs, skos:exactMatch)
- Merges results from different endpoints

---

### 8. **Proof & Validation Engine** (`proof_validation_engine.py`)

**Uses:**
- SPARQL Executor (which uses gen2kgbot)
- ASK queries for validation

**What it does:**
- Validates assertions in the KG
- Generates proof traces
- Checks via direct triple match or reasoning

---

### 9. **Reasoning Narrator** (`reasoning_narrator.py`)

**Uses:**
- No direct gen2kgbot dependency
- Works with outputs from other pipelines

**What it does:**
- Transforms execution traces into explanations
- Builds ReasoningPath models for frontend
- Generates natural language summaries

---

## Testing the Pipelines

### Prerequisites

1. **Setup RDF Endpoint**
   - Download GraphDB Free or Fuseki
   - Start server: `http://localhost:7200`
   - Create a repository
   - Upload test RDF data

2. **Configure Backend**
   ```bash
   # .env
   KG_SPARQL_ENDPOINT_URL=http://localhost:7200/repositories/test-kg
   KG_SHORT_NAME=test-kg
   ```

3. **Setup gen2kgbot Data (Optional for full features)**
   ```bash
   # Create data structure
   mkdir -p gen2kgbot/data/test-kg/example_queries
   mkdir -p gen2kgbot/data/test-kg/preprocessing

   # Run preprocessing (if you have RDF data)
   python -m gen2kgbot.app.preprocessing.compute_embeddings --classes your_classes.txt
   ```

### Test Each Pipeline

```python
# Test 1: SPARQL Executor
from pipelines import SPARQLExecutor

executor = SPARQLExecutor()
results = await executor.execute("SELECT * WHERE { ?s ?p ?o } LIMIT 10")
print(results)

# Test 2: Concept Finder
from pipelines import SemanticConceptFinder

finder = SemanticConceptFinder()
concepts = await finder.find("disease treatment")
print(concepts)

# Test 3: Neighbourhood Retriever
from pipelines import NeighbourhoodRetriever

retriever = NeighbourhoodRetriever()
neighbors = await retriever.retrieve("http://example.org/concept1")
print(neighbors)

# Test 4: Multi-hop Explorer
from pipelines import MultiHopPathExplorer

explorer = MultiHopPathExplorer()
paths = await explorer.find_paths(
    "http://example.org/source",
    "http://example.org/target",
    max_hops=3
)
print(paths)

# Test 5: Ontology Builder
from pipelines import OntologyContextBuilder

builder = OntologyContextBuilder()
context = await builder.build("http://example.org/MyClass")
print(context)

# Test 6: Example Retriever
from pipelines import ExampleBasedPromptRetriever

retriever = ExampleBasedPromptRetriever()
examples = await retriever.retrieve("What are the proteins?")
print(examples)

# Test 7: Federated Connector
from pipelines import FederatedCrossKGConnector

connector = FederatedCrossKGConnector()
connector.register_endpoint("remote_kg", "http://remote:7200/repositories/other")
results = await connector.federated_query(
    "?concept a :Disease",
    "remote_kg",
    "?concept :hasTreatment ?treatment"
)
print(results)

# Test 8: Validation Engine
from pipelines import ProofValidationEngine

engine = ProofValidationEngine()
result = await engine.validate_assertion(
    "http://example.org/Drug1",
    "http://example.org/treats",
    "http://example.org/Disease1"
)
print(result)

# Test 9: Reasoning Narrator
from pipelines import ReasoningNarrator

narrator = ReasoningNarrator()
path = narrator.narrate_concept_exploration(
    {"uri": "http://example.org/Concept1", "label": "Concept 1"},
    {"nodes": [...], "links": [...], "total_neighbors": 5}
)
print(path)
```

## Using with gen2kgbot Scenarios

The pipelines complement gen2kgbot scenarios. Use the adapter:

```python
from adapters.gen2kgbot_adapter import Gen2KGBotAdapter

# For NL2SPARQL (scenarios 1-7)
adapter = Gen2KGBotAdapter(
    kg_endpoint="http://localhost:7200/repositories/test-kg",
    kg_name="test-kg"
)

result = await adapter.execute_scenario(
    scenario_id="scenario_7",
    question="What are the treatments for diabetes?"
)

# Combine with pipelines for post-processing
from pipelines import ReasoningNarrator

narrator = ReasoningNarrator()
reasoning_path = narrator.build_reasoning_path(
    nodes=result.get("nodes", []),
    links=result.get("links", []),
    steps=result.get("steps", [])
)
```

## Key Integration Points

1. **SPARQL Execution**: All pipelines use gen2kgbot's `run_sparql_query()`
2. **Embeddings**: Concept Finder uses gen2kgbot's vector stores
3. **Examples**: Example Retriever loads from gen2kgbot data structure
4. **Config**: Can integrate with gen2kgbot's config_manager

## Notes

- Pipelines work **standalone** without full gen2kgbot setup
- For best results, run gen2kgbot preprocessing first
- Embeddings enable semantic search (vs keyword-only)
- Examples improve NL2SPARQL quality
