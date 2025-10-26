# Wikidata Integration Enhancement Summary

## Date: 2025-01-26

## Overview
Enhanced the `neighbourhood_retriever.py` to properly fetch and display human-readable labels for Wikidata entities and properties, significantly improving user experience for knowledge graph visualization.

## Problem Statement
Initial Wikidata integration returned entity and property IDs (e.g., "Q142", "P17") instead of human-readable labels (e.g., "France", "country"), making the visualization difficult to understand.

## Technical Challenges Encountered

### 1. SPARQL Compatibility Issues
- **Problem**: gen2kgbot's SPARQL CSV parser cannot handle:
  - `SERVICE wikibase:label` clauses
  - `OPTIONAL` clauses for label fetching
  - Complex SPARQL patterns
- **Evidence**: Multiple query failures with error "You did something wrong formulating either the URI or your SPARQL query"
- **Solution**: Simplified SPARQL queries to use only required SELECT variables with FILTER clauses

### 2. Wikidata API Requirements  
- **Problem**: Wikidata's REST API requires a User-Agent header
- **Error**: HTTP 403 with message "Please set a user-agent and respect our robot policy"
- **Solution**: Added User-Agent header: "GRAPE Knowledge Graph Tool/1.0 (https://github.com/grape)"

## Implementation Details

### Files Modified
1. **apps/backend/pipelines/neighbourhood_retriever.py**
   - Added Wikidata endpoint detection: `self.is_wikidata = "wikidata.org" in endpoint`
   - Created `_fetch_wikidata_labels()` method for batch label fetching
   - Created `_fetch_labels()` method using Wikidata REST API
   - Integrated label fetching into main `retrieve()` workflow

2. **apps/backend/requirements.txt**
   - Added `aiohttp>=3.9.0` for async HTTP requests

### Key Methods

#### `_fetch_wikidata_labels(nodes_dict, links)`
- Fetches labels for entities and properties in batch
- Updates node and link dictionaries in-place
- Limits to 50 entities and 20 properties per request for performance
- Includes comprehensive logging for debugging

#### `_fetch_labels(ids, type)`
- Uses Wikidata REST API (`/w/api.php`)
- Batch processes up to 50 IDs per request
- Parameters:
  - `action=wbgetentities`
  - `props=labels`
  - `languages=en`
  - `format=json`
- Returns dict mapping entity ID to English label

### Query Patterns

#### Outgoing Relationships (Wikidata)
```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

SELECT ?property ?target WHERE {
    wd:{entity_id} ?property ?target .
    FILTER(STRSTARTS(STR(?property), "http://www.wikidata.org/prop/direct/"))
    FILTER(STRSTARTS(STR(?target), "http://www.wikidata.org/entity/Q"))
}
LIMIT {limit}
```

#### Incoming Relationships (Wikidata)
```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

SELECT ?property ?source WHERE {
    ?source ?property wd:{entity_id} .
    FILTER(STRSTARTS(STR(?property), "http://www.wikidata.org/prop/direct/"))
    FILTER(STRSTARTS(STR(?source), "http://www.wikidata.org/entity/Q"))
}
LIMIT {limit}
```

## Testing Results

### Test Case 1: Paris (Q90)
- **Total nodes**: 88 (87 neighbors + 1 center)
- **Labeled nodes**: 51 (58% coverage)
- **Sample labels**: 
  - Entities: "Anne Hidalgo", "France", "Europe", "metropolis"
  - Properties: "head of government", "continent", "capital", "official language"

### Test Case 2: Albert Einstein (Q937)
- **Total nodes**: 89
- **Labeled nodes**: 51 (57% coverage)
- **Sample labels**:
  - Entities: "Ulm", "Princeton", "Hermann Einstein", "United States"
  - Properties: Various biographical relationships

### Performance Metrics
- **Label fetch time**: ~200-500ms for 50 entities
- **Total endpoint response**: ~2-3 seconds (including SPARQL queries)
- **Success rate**: 100% (with proper User-Agent)

## API Validation

### Endpoints Tested
1. ✅ `GET /api/health` - Returns healthy status
2. ✅ `GET /api/graph/{graph_id}` - Returns sample graph (3 nodes, 2 links)
3. ✅ `POST /api/wikidata/visualize` - Returns labeled Wikidata graph
4. ✅ `GET /` (Frontend) - HTTP 200, renders correctly

## Lessons Learned

1. **SPARQL Endpoint Variability**: Different SPARQL endpoints have different capabilities. Wikidata's public endpoint has stricter parsing requirements.

2. **REST API as Fallback**: When SPARQL queries become too complex for a parser, using REST APIs for supplementary data (like labels) is a viable approach.

3. **Batch Processing**: Fetching labels in batches (50 entities, 20 properties) balances performance with API limitations.

4. **User-Agent Compliance**: Public APIs like Wikidata enforce robot policies through User-Agent header requirements.

## Future Enhancements

1. **Caching**: Implement label caching to reduce repeated API calls
2. **Language Support**: Extend beyond English labels
3. **Property Label Expansion**: Increase from 20 to 50 property labels per request
4. **Fallback Handling**: Better handling when labels are unavailable (currently shows IDs)
5. **Description Fields**: Fetch and display entity descriptions alongside labels

## Debugging Notes

Test scripts created during development:
- `test_wikidata_query.py` - Tests SPARQL query patterns
- `test_label_query.py` - Tests SPARQL label queries (failed)
- `test_api_labels.py` - Tests Wikidata REST API (successful)

These can be removed or moved to a `debug/` folder if needed.

## Integration Status

✅ **COMPLETE**: Wikidata integration with human-readable labels
- Backend properly fetches labels via REST API
- Frontend GraphView component ready to display labeled graphs
- WikidataInput component accepts URLs and entity IDs
- All validation levels passed (syntax, integration, Docker)
