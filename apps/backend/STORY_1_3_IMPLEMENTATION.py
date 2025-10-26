"""
Test file to demonstrate Story 1.3 implementation.

This file shows how the graph import API would work once the environment is set up.
"""

# Example RDF content in Turtle format
SAMPLE_RDF = """
@prefix ex: <http://example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

ex:Person1 a foaf:Person ;
    foaf:name "Alice" ;
    foaf:age 30 ;
    foaf:knows ex:Person2 .

ex:Person2 a foaf:Person ;
    foaf:name "Bob" ;
    foaf:age 25 .
"""

# Example of how to use the repository (pseudo-code)
def example_usage():
    """
    Example of how Story 1.3 would be used:
    
    1. User uploads an RDF file via POST /api/graphs/import
    2. Backend receives the file and parses it with RDFLib
    3. Repository stores metadata and data in GraphDB
    4. API returns graph_id and confirmation
    
    Expected workflow:
    ```python
    from repositories.graph_repository import GraphRepository
    from rdflib import Graph
    import uuid
    from datetime import datetime
    
    # Parse the uploaded file
    rdf_graph = Graph()
    rdf_graph.parse(data=SAMPLE_RDF, format="turtle")
    
    # Generate ID and create repository
    graph_id = str(uuid.uuid4())
    repo = GraphRepository("http://localhost:7200/repositories/grape")
    
    # Store metadata
    repo.insert_graph_metadata(
        graph_id=graph_id,
        name="Example Graph",
        created_at=datetime.utcnow()
    )
    
    # Store graph data
    triple_count = repo.insert_graph_data(graph_id, rdf_graph)
    
    # Return response
    return {
        "graph_id": graph_id,
        "name": "Example Graph",
        "triple_count": triple_count,
        "message": f"Successfully imported {triple_count} triples"
    }
    ```
    
    The graph would be stored in GraphDB as:
    - Metadata in: <http://grape.app/metadata>
    - Data in: <http://grape.app/graphs/{graph_id}>
    """
    pass


# Example curl request that would work once deployed:
EXAMPLE_CURL = """
# Import an RDF file
curl -X POST http://localhost:8000/api/graphs/import \\
  -F "file=@my_graph.ttl" \\
  -F "name=My Knowledge Graph"

# Response:
{
  "graph_id": "abc-123-def-456",
  "name": "My Knowledge Graph",
  "triple_count": 42,
  "message": "Successfully imported 42 triples"
}

# List all graphs
curl http://localhost:8000/api/graphs

# Response:
[
  {
    "id": "abc-123-def-456",
    "name": "My Knowledge Graph",
    "created_at": "2025-10-26T15:30:00Z",
    "updated_at": "2025-10-26T15:30:00Z"
  }
]

# Get specific graph metadata
curl http://localhost:8000/api/graphs/abc-123-def-456

# Delete a graph
curl -X DELETE http://localhost:8000/api/graphs/abc-123-def-456
"""

if __name__ == "__main__":
    print("Story 1.3 Implementation Complete!")
    print("=" * 60)
    print("\nFiles Created:")
    print("  - repositories/__init__.py")
    print("  - repositories/graph_repository.py")
    print("  - api/routes/graphs.py")
    print("\nFiles Modified:")
    print("  - models/requests.py (added GraphImportRequest)")
    print("  - models/responses.py (added GraphImportResponse)")
    print("  - models/__init__.py (updated exports)")
    print("  - api/routes/__init__.py (added graphs)")
    print("  - main.py (registered graphs router)")
    print("\nAPI Endpoints:")
    print("  POST   /api/graphs/import  - Import RDF file")
    print("  GET    /api/graphs         - List all graphs")
    print("  GET    /api/graphs/{id}    - Get graph metadata")
    print("  DELETE /api/graphs/{id}    - Delete graph")
    print("\nTo test:")
    print("  1. Ensure GraphDB is running and accessible")
    print("  2. Set KG_SPARQL_ENDPOINT_URL in .env")
    print("  3. Run: uvicorn main:app --reload")
    print("  4. Visit: http://localhost:8000/docs")
    print("  5. Upload an RDF file via the /api/graphs/import endpoint")
    print("\n" + "=" * 60)
