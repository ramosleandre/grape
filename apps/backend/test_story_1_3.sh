#!/bin/bash
# Test script for Story 1.3 implementation

echo "==================================================="
echo "Story 1.3 - Testing Guide"
echo "==================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Step 1: Install dependencies${NC}"
echo "Run this command:"
echo "  pip install -r requirements.txt"
echo ""
echo "Press Enter when done..."
read

echo -e "${BLUE}Step 2: Configure environment${NC}"
echo "Create/update .env file with:"
echo ""
echo "KG_SPARQL_ENDPOINT_URL=https://dbpedia.org/sparql"
echo "# OR for local GraphDB:"
echo "# KG_SPARQL_ENDPOINT_URL=http://localhost:7200/repositories/grape"
echo ""
echo "Press Enter when done..."
read

echo -e "${BLUE}Step 3: Start the server${NC}"
echo "Run this in a separate terminal:"
echo "  cd /home/spay/dev/misc/hackathons/google_agent/grape/apps/backend"
echo "  uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Press Enter when server is running..."
read

echo -e "${BLUE}Step 4: Create a test RDF file${NC}"
cat > /tmp/test_graph.ttl << 'EOF'
@prefix ex: <http://example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

ex:Alice rdf:type foaf:Person ;
    foaf:name "Alice Smith" ;
    foaf:age 30 ;
    foaf:knows ex:Bob .

ex:Bob rdf:type foaf:Person ;
    foaf:name "Bob Jones" ;
    foaf:age 25 ;
    foaf:mbox <mailto:bob@example.org> .

ex:Carol rdf:type foaf:Person ;
    foaf:name "Carol Williams" ;
    foaf:knows ex:Alice .
EOF

echo -e "${GREEN}✓ Created test file: /tmp/test_graph.ttl${NC}"
echo ""

echo -e "${BLUE}Step 5: Test the API endpoints${NC}"
echo ""

echo "5.1 - Import the test graph:"
echo "----------------------------"
echo "curl -X POST http://localhost:8000/api/graphs/import \\"
echo "  -F 'file=@/tmp/test_graph.ttl' \\"
echo "  -F 'name=Test Social Network'"
echo ""
echo "Expected response: {"
echo "  \"graph_id\": \"<uuid>\","
echo "  \"name\": \"Test Social Network\","
echo "  \"triple_count\": 8,"
echo "  \"message\": \"Successfully imported 8 triples\""
echo "}"
echo ""
echo "Press Enter to run this test..."
read

RESPONSE=$(curl -s -X POST http://localhost:8000/api/graphs/import \
  -F "file=@/tmp/test_graph.ttl" \
  -F "name=Test Social Network")

if [ $? -eq 0 ]; then
  echo -e "${GREEN}✓ Response:${NC}"
  echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
  
  # Extract graph_id for next tests
  GRAPH_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('graph_id', ''))" 2>/dev/null)
  echo ""
  echo -e "${GREEN}✓ Graph ID: $GRAPH_ID${NC}"
else
  echo -e "${YELLOW}⚠ Could not connect to API. Make sure server is running.${NC}"
fi
echo ""

echo "5.2 - List all graphs:"
echo "----------------------"
echo "curl http://localhost:8000/api/graphs"
echo ""
echo "Press Enter to run..."
read

curl -s http://localhost:8000/api/graphs | python3 -m json.tool 2>/dev/null
echo ""

if [ ! -z "$GRAPH_ID" ]; then
  echo "5.3 - Get specific graph metadata:"
  echo "----------------------------------"
  echo "curl http://localhost:8000/api/graphs/$GRAPH_ID"
  echo ""
  echo "Press Enter to run..."
  read
  
  curl -s http://localhost:8000/api/graphs/$GRAPH_ID | python3 -m json.tool 2>/dev/null
  echo ""
fi

echo -e "${BLUE}Step 6: Test via Swagger UI${NC}"
echo "Open: http://localhost:8000/docs"
echo ""
echo "Try the following:"
echo "  1. Click on 'POST /api/graphs/import'"
echo "  2. Click 'Try it out'"
echo "  3. Upload /tmp/test_graph.ttl"
echo "  4. Enter a name"
echo "  5. Click 'Execute'"
echo ""

echo -e "${GREEN}==================================================="
echo "Testing Complete!"
echo "===================================================${NC}"
echo ""
echo "Next steps:"
echo "  - Check the Swagger UI at http://localhost:8000/docs"
echo "  - Review logs in the terminal where uvicorn is running"
echo "  - Query GraphDB directly to verify data was stored"
echo ""
