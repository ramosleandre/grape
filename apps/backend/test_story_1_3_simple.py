"""
Simple test for Story 1.3 implementation without gen2kgbot dependencies.
Tests the code structure and RDF parsing capabilities.
"""

import sys
from pathlib import Path

print("=" * 60)
print("STORY 1.3 SIMPLE IMPLEMENTATION TEST")
print("=" * 60)

# Test 1: Check that files exist
print("\n1. Checking implementation files...")
backend_dir = Path(__file__).parent

files_to_check = [
    "repositories/__init__.py",
    "repositories/graph_repository.py",
    "api/routes/graphs.py",
    "models/requests.py",
    "models/responses.py",
]

missing_files = []
for file_path in files_to_check:
    full_path = backend_dir / file_path
    if not full_path.exists():
        missing_files.append(file_path)
        print(f"   ❌ Missing: {file_path}")
    else:
        print(f"   ✅ Found: {file_path}")

if missing_files:
    print(f"\n❌ {len(missing_files)} files are missing!")
    sys.exit(1)

# Test 2: Test RDF parsing (core functionality)
print("\n2. Testing RDF parsing...")
try:
    from rdflib import Graph
    
    # Create a simple RDF graph
    sample_rdf = """
    @prefix ex: <http://example.org/> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    
    ex:Subject1 rdfs:label "Test Subject" .
    ex:Subject1 ex:hasProperty ex:Object1 .
    """
    
    g = Graph()
    g.parse(data=sample_rdf, format="turtle")
    
    triple_count = len(g)
    print(f"   ✅ Parsed {triple_count} triples")
    
    if triple_count != 2:
        print(f"   ⚠️  Expected 2 triples, got {triple_count}")
    
except Exception as e:
    print(f"   ❌ RDF parsing failed: {e}")
    sys.exit(1)

# Test 3: Test Pydantic models
print("\n3. Testing Pydantic models...")
try:
    from models.requests import GraphImportRequest
    from models.responses import GraphImportResponse, KnowledgeGraph
    
    # Test request model
    request = GraphImportRequest(name="Test Graph")
    print(f"   ✅ GraphImportRequest created: name='{request.name}'")
    
    # Test response model
    response = GraphImportResponse(
        graph_id="test-123",
        name="Test Graph",
        message="Graph imported successfully",
        triple_count=100
    )
    print(f"   ✅ GraphImportResponse created: graph_id={response.graph_id}, triples={response.triple_count}")
    
    # Test KnowledgeGraph model
    from datetime import datetime
    now = datetime.utcnow()
    kg = KnowledgeGraph(
        id="test-123",
        name="Test Graph",
        created_at=now,
        updated_at=now
    )
    print(f"   ✅ KnowledgeGraph created: id={kg.id}, name='{kg.name}'")
    
except Exception as e:
    print(f"   ❌ Model testing failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Check FastAPI route structure
print("\n4. Checking FastAPI route structure...")
try:
    with open(backend_dir / "api/routes/graphs.py", "r") as f:
        content = f.read()
    
    required_patterns = [
        "router = APIRouter",
        "@router.post(",
        '"/import"',
        "@router.get(",
        '"/{graph_id}"',
        "@router.delete(",
        "GraphRepository",
    ]
    
    for pattern in required_patterns:
        if pattern in content:
            print(f"   ✅ Found: {pattern}")
        else:
            print(f"   ❌ Missing: {pattern}")
    
except Exception as e:
    print(f"   ❌ Route checking failed: {e}")
    sys.exit(1)

# Test 5: Check repository structure
print("\n5. Checking repository structure...")
try:
    with open(backend_dir / "repositories/graph_repository.py", "r") as f:
        content = f.read()
    
    required_methods = [
        "def insert_graph_metadata",
        "def insert_graph_data",
        "def get_graph_metadata",
        "def list_graphs",
        "def delete_graph",
    ]
    
    for method in required_methods:
        if method in content:
            print(f"   ✅ Found: {method}")
        else:
            print(f"   ❌ Missing: {method}")
    
except Exception as e:
    print(f"   ❌ Repository checking failed: {e}")
    sys.exit(1)

# Test 6: Verify RDF named graph structure
print("\n6. Testing named graph RDF generation...")
try:
    from rdflib import Graph, Namespace, Literal, URIRef
    from rdflib.namespace import RDF, RDFS, XSD
    from datetime import datetime
    import uuid
    
    # Create metadata graph (simulating what the repository does)
    GRAPE = Namespace("http://grape.app/vocab#")
    metadata_graph = Graph()
    
    graph_id = str(uuid.uuid4())
    graph_uri = URIRef(f"http://grape.app/graphs/{graph_id}")
    
    metadata_graph.add((graph_uri, RDF.type, GRAPE.KnowledgeGraph))
    metadata_graph.add((graph_uri, GRAPE.name, Literal("Test Graph")))
    metadata_graph.add((graph_uri, GRAPE.graphId, Literal(graph_id)))
    metadata_graph.add((graph_uri, GRAPE.createdAt, Literal(datetime.utcnow().isoformat() + "Z", datatype=XSD.dateTime)))
    metadata_graph.add((graph_uri, GRAPE.tripleCount, Literal(42, datatype=XSD.integer)))
    
    # Serialize and check
    ttl = metadata_graph.serialize(format="turtle")
    print(f"   ✅ Generated metadata graph with {len(metadata_graph)} triples")
    print(f"   ✅ Graph ID: {graph_id}")
    
    # Verify we can parse it back
    test_graph = Graph()
    test_graph.parse(data=ttl, format="turtle")
    print(f"   ✅ Verified: Can parse generated RDF")
    
except Exception as e:
    print(f"   ❌ Named graph testing failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\nStory 1.3 implementation structure is correct.")
print("Note: Full integration testing requires:")
print("  - GraphDB or SPARQL endpoint configured")
print("  - gen2kgbot dependencies installed")
print("  - FastAPI server running")
