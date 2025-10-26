# 🧪 GRAPE Knowledge Graph Visualization - Testing Guide

## Quick Start

```bash
# 1. Start the services
cd /Users/ymehili/dev/grape
make up

# 2. Wait for services to be healthy (~10 seconds)
docker ps

# 3. Open the application
open http://localhost:3000
```

## 📋 Complete Test Checklist

### ✅ Backend API Tests

#### 1. Health Check
```bash
curl http://localhost:8000/api/health | python3 -m json.tool
```
**Expected**: `{"status": "healthy", "version": "0.1.0", ...}`

#### 2. Sample Graph Endpoint
```bash
curl http://localhost:8000/api/graph/test123 | python3 -m json.tool
```
**Expected**: 3 nodes, 2 links with sample data

#### 3. Wikidata Entity by ID
```bash
curl -X POST http://localhost:8000/api/wikidata/visualize \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "Q90"}' | python3 -m json.tool
```
**Expected**: 
- ~88 nodes about Paris
- ~51 nodes with readable labels (57% coverage)
- Labels like "France", "Europe", "Anne Hidalgo"

#### 4. Wikidata Entity by URL
```bash
curl -X POST http://localhost:8000/api/wikidata/visualize \
  -H "Content-Type: application/json" \
  -d '{"wikidata_url": "https://www.wikidata.org/wiki/Q937"}' | python3 -m json.tool
```
**Expected**: 
- ~94 nodes about Albert Einstein
- Labels like "Ulm", "Princeton", "Hermann Einstein"

### 🌐 Frontend Tests

#### 1. Home Page
```bash
open http://localhost:3000
```
**Expected**:
- ✅ GRAPE logo and welcome message
- ✅ Three feature cards (Interactive Visualization, AI-Powered Querying, Transparent Reasoning)
- ✅ "Open Workspace" button
- ✅ Placeholder buttons (Import RDF, Create from PDF, Create from URL)

#### 2. Workspace Page
```bash
open http://localhost:3000/workspace
```
**Expected**:
- ✅ Graph visualization area (empty initially)
- ✅ Wikidata Input panel on the right
- ✅ Input field with placeholder "Enter Wikidata URL or entity ID..."
- ✅ "Visualize" button

### 🎯 Interactive Frontend Testing

#### Test Case 1: Visualize Paris
1. Navigate to http://localhost:3000/workspace
2. In the Wikidata Input panel, enter: `Q90` or `https://www.wikidata.org/wiki/Q90`
3. Click "Visualize"

**Expected Results**:
- ✅ Graph loads with ~88 nodes
- ✅ Nodes show readable labels: "Paris", "France", "Europe", etc.
- ✅ You can pan and zoom the graph
- ✅ Nodes are colored (center node different from neighbors)
- ✅ Hovering shows node labels
- ✅ Links connect nodes showing relationships

#### Test Case 2: Visualize Albert Einstein
1. Clear the input and enter: `Q937`
2. Click "Visualize"

**Expected Results**:
- ✅ Graph updates with ~94 nodes
- ✅ Shows labels: "Albert Einstein", "Ulm", "Princeton", "Hermann Einstein"
- ✅ Smooth transition to new graph

#### Test Case 3: Visualize from URL
1. Enter: `https://www.wikidata.org/wiki/Q5582` (Vincent van Gogh)
2. Click "Visualize"

**Expected Results**:
- ✅ Graph loads with ~90 nodes
- ✅ Shows labels: "Vincent van Gogh", "Zundert", "Auvers-sur-Oise"

#### Test Case 4: Test Different Entities

Try these Wikidata entities:
- `Q1299` - The Beatles (music group)
- `Q5` - human (concept)
- `Q42` - Douglas Adams (author)
- `Q2807` - Madrid (city)
- `Q5916` - Marie Curie (scientist)

### 🔍 Visual Inspection Checklist

When visualizing a graph, verify:

- [ ] **Nodes**:
  - Center node is visually distinct (different size/color)
  - Neighbor nodes have readable labels (not just Q-IDs)
  - Nodes without labels show their entity ID as fallback
  - Node size is consistent

- [ ] **Links**:
  - Lines connect related nodes
  - Links don't overlap excessively
  - Graph is readable (not too cluttered)

- [ ] **Interactions**:
  - Pan: Click and drag to move the graph
  - Zoom: Scroll to zoom in/out
  - Auto-layout: Graph organizes itself
  - Hover: Shows node label on hover

- [ ] **Performance**:
  - Initial load: < 5 seconds
  - Graph rendering: Smooth, no lag
  - Interactions: Responsive

### 🐛 Troubleshooting

#### Backend not responding
```bash
# Check container status
docker ps

# View logs
docker logs grape-api

# Restart
make down && make up
```

#### Frontend not loading
```bash
# Check container status
docker ps | grep grape-web

# View logs
docker logs grape-web

# Restart
make down && make up
```

#### No labels showing (all Q-IDs)
```bash
# Check backend logs for label fetching
docker logs grape-api | grep -i "label"

# Should see:
# - "Fetching labels for X entities and Y properties"
# - "Fetched N entity labels"
# - "Fetched M property labels"
```

#### Wikidata API rate limiting
If you see 429 errors:
- Wait 60 seconds before making another request
- Reduce the number of test requests
- The API has rate limits for the public endpoint

### 📊 Performance Benchmarks

**Typical Response Times**:
- Health check: < 50ms
- Sample graph: < 100ms
- Wikidata visualization: 2-4 seconds
  - SPARQL query: 1-2 seconds
  - Label fetching: 0.5-1 second
  - Processing: 0.5-1 second

**Expected Coverage**:
- Nodes returned: 80-100 per entity
- Label coverage: 50-60% (Wikidata API batch limit)
- Links returned: 100 (max limit)

### 🧹 Cleanup

```bash
# Stop services
make down

# Remove all containers and volumes
make clean

# Rebuild from scratch
make build && make up
```

### 📝 Test Automation Script

Save this as `test_all.sh`:

```bash
#!/bin/bash
set -e

echo "🧪 Starting GRAPE Test Suite"
echo "=============================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo -e "\n📍 Test 1: Backend Health Check"
if curl -s http://localhost:8000/api/health | grep -q "healthy"; then
    echo -e "${GREEN}✅ PASS${NC}"
else
    echo -e "${RED}❌ FAIL${NC}"
    exit 1
fi

# Test 2: Sample Graph
echo -e "\n📍 Test 2: Sample Graph Endpoint"
NODES=$(curl -s http://localhost:8000/api/graph/test123 | python3 -c "import sys,json;print(len(json.load(sys.stdin)['nodes']))")
if [ "$NODES" -eq 3 ]; then
    echo -e "${GREEN}✅ PASS${NC} - Got 3 nodes"
else
    echo -e "${RED}❌ FAIL${NC} - Expected 3 nodes, got $NODES"
    exit 1
fi

# Test 3: Wikidata - Paris
echo -e "\n📍 Test 3: Wikidata Entity (Paris)"
PARIS_NODES=$(curl -s -X POST http://localhost:8000/api/wikidata/visualize \
    -H "Content-Type: application/json" \
    -d '{"entity_id": "Q90"}' | \
    python3 -c "import sys,json;d=json.load(sys.stdin);print(len(d['nodes']))")
if [ "$PARIS_NODES" -gt 50 ]; then
    echo -e "${GREEN}✅ PASS${NC} - Got $PARIS_NODES nodes"
else
    echo -e "${RED}❌ FAIL${NC} - Expected >50 nodes, got $PARIS_NODES"
    exit 1
fi

# Test 4: Wikidata - URL format
echo -e "\n📍 Test 4: Wikidata URL Format"
URL_NODES=$(curl -s -X POST http://localhost:8000/api/wikidata/visualize \
    -H "Content-Type: application/json" \
    -d '{"wikidata_url": "https://www.wikidata.org/wiki/Q937"}' | \
    python3 -c "import sys,json;d=json.load(sys.stdin);print(len(d['nodes']))")
if [ "$URL_NODES" -gt 50 ]; then
    echo -e "${GREEN}✅ PASS${NC} - Got $URL_NODES nodes"
else
    echo -e "${RED}❌ FAIL${NC} - Expected >50 nodes, got $URL_NODES"
    exit 1
fi

# Test 5: Frontend
echo -e "\n📍 Test 5: Frontend Health"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
if [ "$STATUS" -eq 200 ]; then
    echo -e "${GREEN}✅ PASS${NC} - HTTP $STATUS"
else
    echo -e "${RED}❌ FAIL${NC} - Expected 200, got $STATUS"
    exit 1
fi

echo -e "\n=============================="
echo -e "${GREEN}🎉 All tests passed!${NC}"
echo -e "\n🌐 Open http://localhost:3000 to test the UI"
```

Make it executable and run:
```bash
chmod +x test_all.sh
./test_all.sh
```

## 🎓 What This Feature Does

**Story 2.1: Basic Knowledge Graph Visualization** enables:

1. **Wikidata Integration**: Fetch and visualize any Wikidata entity
2. **Human-Readable Labels**: Shows "France" instead of "Q142"
3. **Interactive Graph**: Pan, zoom, explore relationships
4. **1-Hop Neighbors**: See all directly connected entities
5. **RESTful API**: Backend endpoints for graph data

**Key Innovation**: 
- Wikidata SPARQL endpoint has limitations with label fetching
- Solution: Hybrid approach using SPARQL for structure + REST API for labels
- Achieves 50-60% label coverage (limited by API batch size)
