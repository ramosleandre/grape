# Story 1.3 Testing Guide

This guide explains how to test the Knowledge Graph Import API implementation.

## Test Status

✅ **Code Structure Tests**: PASSED (all files present, models valid, routes defined)
⏳ **Integration Tests**: Require GraphDB setup
⏳ **End-to-End Tests**: Require running FastAPI server

## Prerequisites

### Minimal Setup (Already Completed)
```bash
pip install rdflib fastapi pydantic pydantic-settings python-dotenv pyyaml python-multipart
```

### Full Setup (For Integration Testing)
```bash
# Install all dependencies (requires fixing spacy/blis issue)
pip install -r requirements.txt

# OR install without spacy for now
pip install -r requirements.txt --no-deps
pip install fastapi uvicorn rdflib pydantic pydantic-settings python-dotenv pyyaml python-multipart httpx
```

## Test Levels

### 1. Code Structure Test ✅ PASSED

Tests that all implementation files exist and have the correct structure:

```bash
cd /home/spay/dev/misc/hackathons/google_agent/grape/apps/backend
python test_story_1_3_simple.py
```

**What it validates:**
- All implementation files are present
- RDF parsing works with rdflib
- Pydantic models are correctly defined
- FastAPI routes are declared
- Repository methods exist
- Named graph RDF generation works

### 2. Unit Tests (Without GraphDB)

Create mocked unit tests that don't require a real GraphDB instance:

```bash
# TODO: Create test_graph_repository_unit.py with mocked SPARQL responses
# TODO: Create test_graph_routes_unit.py with mocked repository
```

### 3. Integration Tests (With GraphDB)

**Setup GraphDB:**

Option A: Use Docker (Recommended for testing)
```bash
docker run -d \
  --name graphdb \
  -p 7200:7200 \
  ontotext/graphdb:10.0.0
```

Option B: Use public SPARQL endpoint (Read-only, testing limited)
- DBpedia: http://dbpedia.org/sparql
- Wikidata: https://query.wikidata.org/sparql

**Configure environment:**

```bash
# Set SPARQL endpoint in gen2kgbot config
# Edit apps/backend/gen2kgbot/config/config.yaml
# OR set environment variable
export SPARQL_ENDPOINT_URL="http://localhost:7200/repositories/test"
```

**Run integration tests:**

```bash
# TODO: Create test_graph_repository_integration.py
# Tests actual SPARQL INSERT/SELECT/DELETE operations
python -m pytest tests/test_graph_repository_integration.py
```

### 4. End-to-End API Tests

**Start the FastAPI server:**

```bash
cd /home/spay/dev/misc/hackathons/google_agent/grape/apps/backend
uvicorn main:app --reload --port 8000
```

**Test with curl:**

```bash
# Test 1: Import a graph
curl -X POST http://localhost:8000/api/graphs/import \
  -F "file=@sample_graph.ttl" \
  -F "name=Alzheimer's Research Data"

# Example response:
# {
#   "graph_id": "abc-123-def",
#   "name": "Alzheimer's Research Data",
#   "triple_count": 14,
#   "message": "Successfully imported 14 triples"
# }

# Test 2: List all graphs
curl http://localhost:8000/api/graphs/

# Test 3: Get specific graph metadata
curl http://localhost:8000/api/graphs/{graph_id}

# Test 4: Delete a graph
curl -X DELETE http://localhost:8000/api/graphs/{graph_id}
```

**Test with Python requests:**

```python
import requests

# Import graph
with open('sample_graph.ttl', 'rb') as f:
    files = {'file': f}
    data = {'name': 'Test Graph'}
    response = requests.post('http://localhost:8000/api/graphs/import', files=files, data=data)
    print(response.json())

# List graphs
response = requests.get('http://localhost:8000/api/graphs/')
print(response.json())
```

**Test with the built-in example:**

```bash
cd /home/spay/dev/misc/hackathons/google_agent/grape/apps/backend
python STORY_1_3_IMPLEMENTATION.py
```

## Sample Test Data

A sample RDF file is provided: `sample_graph.ttl`

It contains 14 triples representing:
- Alzheimer's Disease entity
- Related drug (Donepezil)
- Associated gene (APOE ε4)
- Symptoms and biological systems

## Known Issues

### 1. Missing gen2kgbot Dependencies

**Problem:** `run_sparql_query` requires gen2kgbot setup with LangChain, HuggingFace, etc.

**Workaround:**
- For unit testing: Mock the `run_sparql_query` function
- For integration testing: Install minimal gen2kgbot deps or use a test SPARQL client

### 2. Spacy/Blis Compilation Issue

**Problem:** `pip install spacy` fails with AVX-512 compilation error

**Workaround:**
- Spacy is only needed for gen2kgbot NLP features (not Story 1.3)
- Install deps without spacy for now
- File issue with gen2kgbot to make spacy optional

### 3. No GraphDB Instance

**Problem:** No SPARQL endpoint configured

**Solutions:**
1. Run GraphDB in Docker (see above)
2. Use public endpoint (limited write access)
3. Mock SPARQL responses for testing

## Next Steps

1. ✅ Code structure validation complete
2. ⏳ Set up GraphDB instance (Docker recommended)
3. ⏳ Configure SPARQL endpoint in gen2kgbot config
4. ⏳ Create unit tests with mocked dependencies
5. ⏳ Create integration tests with real GraphDB
6. ⏳ Run end-to-end API tests

## Continuous Testing

Once the environment is set up, you can run:

```bash
# Quick validation (no dependencies required)
python test_story_1_3_simple.py

# Full test suite (requires GraphDB)
pytest tests/ -v

# With coverage
pytest tests/ --cov=repositories --cov=api/routes/graphs
```

## Testing Checklist

- [x] Code structure validation
- [ ] Repository unit tests (mocked)
- [ ] API route unit tests (mocked)
- [ ] Integration tests with GraphDB
- [ ] End-to-end API tests
- [ ] Error handling tests
- [ ] Large file upload tests
- [ ] Concurrent import tests
- [ ] Invalid RDF format tests
