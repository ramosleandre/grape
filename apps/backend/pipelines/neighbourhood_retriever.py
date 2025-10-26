"""
Neighbourhood Retriever Pipeline
Get all direct connections (1-hop) of a concept in the KG.
"""

from typing import List, Dict, Any, Optional
from pipelines.sparql_query_executor import SPARQLExecutor
from core.config import settings
import logging

logger = logging.getLogger(__name__)


class NeighbourhoodRetriever:
    """Retrieve direct neighbors of a concept."""

    def __init__(self, endpoint: Optional[str] = None):
        self.executor = SPARQLExecutor(endpoint)
        self.endpoint = endpoint or settings.kg_sparql_endpoint_url
        self.is_wikidata = "wikidata.org" in (self.endpoint or "")

    async def retrieve(
        self,
        concept_uri: str,
        max_neighbors: int = 100,
        include_incoming: bool = True,
        include_outgoing: bool = True,
    ) -> Dict[str, Any]:
        """
        Get all 1-hop neighbors of a concept.

        Args:
            concept_uri: URI of the concept
            max_neighbors: Max neighbors to retrieve
            include_incoming: Include incoming edges
            include_outgoing: Include outgoing edges

        Returns:
            Dict with nodes and links
        """
        nodes = []
        links = []

        # Get outgoing relationships
        if include_outgoing:
            outgoing = await self._get_outgoing(concept_uri, max_neighbors)
            nodes.extend(outgoing["nodes"])
            links.extend(outgoing["links"])

        # Get incoming relationships
        if include_incoming:
            incoming = await self._get_incoming(concept_uri, max_neighbors)
            nodes.extend(incoming["nodes"])
            links.extend(incoming["links"])

        # Deduplicate nodes
        unique_nodes = {n["id"]: n for n in nodes}

        # For Wikidata, fetch labels in a separate batch query
        if self.is_wikidata and unique_nodes:
            await self._fetch_wikidata_labels(unique_nodes, links)

        return {
            "center_node": concept_uri,
            "nodes": list(unique_nodes.values()),
            "links": links,
            "total_neighbors": len(unique_nodes),
        }

    async def retrieve_multi_hop(
        self,
        concept_uri: str,
        max_depth: int = 2,
        max_neighbors_per_node: int = 20,
        include_incoming: bool = True,
        include_outgoing: bool = True,
    ) -> Dict[str, Any]:
        """
        Get multi-hop neighbors of a concept (recursive traversal).

        Args:
            concept_uri: URI of the starting concept
            max_depth: Maximum depth to traverse (1 = direct neighbors only)
            max_neighbors_per_node: Max neighbors to retrieve per node
            include_incoming: Include incoming edges
            include_outgoing: Include outgoing edges

        Returns:
            Dict with nodes and links from all depths
        """
        all_nodes = {}
        all_links = []
        visited = set()
        
        # Track nodes to explore at each level
        current_level = {concept_uri}
        
        for depth in range(max_depth):
            if not current_level:
                break
                
            next_level = set()
            logger.info(f"Exploring depth {depth + 1} with {len(current_level)} nodes")
            
            for node_uri in current_level:
                if node_uri in visited:
                    continue
                    
                visited.add(node_uri)
                
                # Get 1-hop neighborhood for this node
                neighborhood = await self.retrieve(
                    concept_uri=node_uri,
                    max_neighbors=max_neighbors_per_node,
                    include_incoming=include_incoming,
                    include_outgoing=include_outgoing,
                )
                
                # Add nodes and links
                for node in neighborhood["nodes"]:
                    node_id = node["id"]
                    if node_id not in all_nodes:
                        all_nodes[node_id] = node
                        # Add to next level if we haven't reached max depth
                        if depth + 1 < max_depth:
                            next_level.add(node_id)
                
                for link in neighborhood["links"]:
                    # Avoid duplicate links
                    link_key = f"{link['source']}-{link['relation']}-{link['target']}"
                    if not any(
                        f"{l['source']}-{l['relation']}-{l['target']}" == link_key 
                        for l in all_links
                    ):
                        all_links.append(link)
            
            current_level = next_level
            logger.info(f"Found {len(all_nodes)} total nodes, queuing {len(next_level)} for next level")
        
        return {
            "center_node": concept_uri,
            "nodes": list(all_nodes.values()),
            "links": all_links,
            "total_neighbors": len(all_nodes),
            "depth": max_depth,
        }

    async def _fetch_wikidata_labels(self, nodes_dict: Dict[str, Dict], links: List[Dict]) -> None:
        """Fetch labels for Wikidata entities and properties in batch."""
        try:
            # Get unique entity and property URIs
            entity_ids = [uri.split("/")[-1] for uri in nodes_dict.keys()]
            property_ids = list(set([link["relation"].split("/")[-1] for link in links]))

            logger.info(f"Fetching labels for {len(entity_ids)} entities and {len(property_ids)} properties")

            # Fetch entity labels
            if entity_ids:
                entity_labels = await self._fetch_labels(
                    entity_ids[:50], "entity"
                )  # Limit for performance
                logger.info(f"Fetched {len(entity_labels)} entity labels")
                for uri, node in nodes_dict.items():
                    entity_id = uri.split("/")[-1]
                    if entity_id in entity_labels:
                        node["label"] = entity_labels[entity_id]
                        logger.debug(f"Set label for {entity_id}: {entity_labels[entity_id]}")

            # Fetch property labels
            if property_ids:
                prop_labels = await self._fetch_labels(property_ids[:20], "property")
                logger.info(f"Fetched {len(prop_labels)} property labels")
                for link in links:
                    prop_id = link["relation"].split("/")[-1]
                    if prop_id in prop_labels:
                        link["label"] = prop_labels[prop_id]
                        logger.debug(f"Set label for property {prop_id}: {prop_labels[prop_id]}")

        except Exception as e:
            logger.warning(f"Failed to fetch Wikidata labels: {e}")
            # Continue without labels

    async def _fetch_labels(self, ids: List[str], type: str = "entity") -> Dict[str, str]:
        """Fetch labels for a list of Wikidata IDs using the Wikidata API."""
        if not ids:
            return {}

        import aiohttp

        labels = {}
        
        # Wikidata API allows up to 50 entities per request
        batch_size = 50
        for i in range(0, len(ids), batch_size):
            batch_ids = ids[i:i+batch_size]
            
            # Use Wikidata API to get labels
            url = "https://www.wikidata.org/w/api.php"
            params = {
                "action": "wbgetentities",
                "ids": "|".join(batch_ids),
                "props": "labels",
                "languages": "en",
                "format": "json"
            }
            
            headers = {
                "User-Agent": "GRAPE Knowledge Graph Tool/1.0 (https://github.com/grape)"
            }
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params, headers=headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            entities = data.get("entities", {})
                            for entity_id, entity_data in entities.items():
                                if "labels" in entity_data and "en" in entity_data["labels"]:
                                    labels[entity_id] = entity_data["labels"]["en"]["value"]
                        else:
                            logger.warning(f"Wikidata API returned status {response.status}")
            except Exception as e:
                logger.warning(f"Failed to fetch {type} labels for batch: {e}")
                continue

        return labels

    async def _get_outgoing(self, concept_uri: str, limit: int) -> Dict[str, List[Dict]]:
        """Get outgoing relationships."""

        if self.is_wikidata:
            # Wikidata-specific query using wdt: (truthy statements)
            # Extract entity ID from URI (e.g., Q90 from http://www.wikidata.org/entity/Q90)
            entity_id = concept_uri.split("/")[-1]

            query = f"""
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>
            
            SELECT ?property ?target WHERE {{
                wd:{entity_id} ?property ?target .
                FILTER(STRSTARTS(STR(?property), "http://www.wikidata.org/prop/direct/"))
                FILTER(STRSTARTS(STR(?target), "http://www.wikidata.org/entity/Q"))
            }}
            LIMIT {limit}
            """
        else:
            # Generic SPARQL query for other endpoints
            query = f"""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?property ?target ?targetLabel ?propertyLabel WHERE {{
                <{concept_uri}> ?property ?target .
                FILTER(isURI(?target))
                OPTIONAL {{ ?target rdfs:label ?targetLabel }}
                OPTIONAL {{ ?property rdfs:label ?propertyLabel }}
            }}
            LIMIT {limit}
            """

        try:
            results = await self.executor.execute(query)
            nodes = []
            links = []

            for r in results:
                target_uri = r.get("target", "")
                if not target_uri:
                    continue

                nodes.append(
                    {
                        "id": target_uri,
                        "label": r.get("targetLabel", target_uri.split("/")[-1]),
                        "type": "entity",
                    }
                )
                links.append(
                    {
                        "source": concept_uri,
                        "target": target_uri,
                        "relation": r.get("property", ""),
                        "label": r.get("propertyLabel", r.get("property", "").split("/")[-1]),
                    }
                )

            return {"nodes": nodes, "links": links}

        except Exception as e:
            logger.error(f"Failed to get outgoing relationships: {e}")
            return {"nodes": [], "links": []}

    async def _get_incoming(self, concept_uri: str, limit: int) -> Dict[str, List[Dict]]:
        """Get incoming relationships."""

        if self.is_wikidata:
            # Wikidata-specific query for incoming relationships
            entity_id = concept_uri.split("/")[-1]

            query = f"""
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>
            
            SELECT ?property ?source WHERE {{
                ?source ?property wd:{entity_id} .
                FILTER(STRSTARTS(STR(?property), "http://www.wikidata.org/prop/direct/"))
                FILTER(STRSTARTS(STR(?source), "http://www.wikidata.org/entity/Q"))
            }}
            LIMIT {limit}
            """
        else:
            # Generic SPARQL query for other endpoints
            query = f"""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?property ?source ?sourceLabel ?propertyLabel WHERE {{
                ?source ?property <{concept_uri}> .
                FILTER(isURI(?source))
                OPTIONAL {{ ?source rdfs:label ?sourceLabel }}
                OPTIONAL {{ ?property rdfs:label ?propertyLabel }}
            }}
            LIMIT {limit}
            """

        try:
            results = await self.executor.execute(query)
            nodes = []
            links = []

            for r in results:
                source_uri = r.get("source", "")
                if not source_uri:
                    continue

                nodes.append(
                    {
                        "id": source_uri,
                        "label": r.get("sourceLabel", source_uri.split("/")[-1]),
                        "type": "entity",
                    }
                )
                links.append(
                    {
                        "source": source_uri,
                        "target": concept_uri,
                        "relation": r.get("property", ""),
                        "label": r.get("propertyLabel", r.get("property", "").split("/")[-1]),
                    }
                )

            return {"nodes": nodes, "links": links}

        except Exception as e:
            logger.error(f"Failed to get incoming relationships: {e}")
            return {"nodes": [], "links": []}
