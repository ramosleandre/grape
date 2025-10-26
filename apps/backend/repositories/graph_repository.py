"""
Graph Repository - Data access layer for knowledge graph operations.

Handles:
- Storing graph metadata
- Inserting graph data into named graphs
- Retrieving graph information
- Managing graph lifecycle
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD
import sys
from pathlib import Path

# Add gen2kgbot to path
gen2kgbot_path = Path(__file__).parent.parent / "gen2kgbot"
if str(gen2kgbot_path) not in sys.path:
    sys.path.insert(0, str(gen2kgbot_path))

from app.utils.sparql_toolkit import run_sparql_query

logger = logging.getLogger(__name__)

# Grape namespace for metadata
GRAPE = Namespace("http://grape.app/vocab#")
GRAPE_GRAPHS = "http://grape.app/graphs/"
GRAPE_METADATA = "http://grape.app/metadata"


class GraphRepository:
    """Repository for managing knowledge graphs in GraphDB."""

    def __init__(self, endpoint_url: str):
        """
        Initialize the graph repository.

        Args:
            endpoint_url: SPARQL endpoint URL for GraphDB
        """
        self.endpoint_url = endpoint_url
        if not self.endpoint_url:
            raise ValueError("SPARQL endpoint URL is required")

    def insert_graph_metadata(
        self,
        graph_id: str,
        name: str,
        created_at: datetime,
    ) -> bool:
        """
        Store graph metadata as RDF triples in the metadata named graph.

        Args:
            graph_id: Unique identifier for the graph
            name: Human-readable name of the graph
            created_at: Creation timestamp

        Returns:
            True if successful, False otherwise
        """
        graph_uri = URIRef(f"{GRAPE_GRAPHS}{graph_id}")
        created_literal = Literal(created_at.isoformat(), datatype=XSD.dateTime)

        sparql_insert = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX grape: <http://grape.app/vocab#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

INSERT DATA {{
  GRAPH <{GRAPE_METADATA}> {{
    <{graph_uri}> rdf:type grape:KnowledgeGraph ;
                  grape:name "{name}" ;
                  grape:createdAt "{created_at.isoformat()}"^^xsd:dateTime ;
                  grape:updatedAt "{created_at.isoformat()}"^^xsd:dateTime .
  }}
}}
"""

        try:
            logger.info(f"Inserting metadata for graph {graph_id}")
            run_sparql_query(sparql_insert, self.endpoint_url)
            logger.info(f"Successfully inserted metadata for graph {graph_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to insert graph metadata: {e}")
            raise

    def insert_graph_data(
        self,
        graph_id: str,
        rdf_graph: Graph,
    ) -> int:
        """
        Insert RDF triples into a named graph in GraphDB.

        Args:
            graph_id: Unique identifier for the graph
            rdf_graph: RDFLib Graph containing the triples to insert

        Returns:
            Number of triples inserted
        """
        graph_uri = f"{GRAPE_GRAPHS}{graph_id}"
        
        # Serialize the graph to N-Triples format for insertion
        # N-Triples is simple and reliable for SPARQL INSERT
        triples_nt = rdf_graph.serialize(format="nt")
        
        # Count triples
        triple_count = len(rdf_graph)
        
        if triple_count == 0:
            logger.warning(f"No triples to insert for graph {graph_id}")
            return 0

        # Build SPARQL INSERT DATA query
        sparql_insert = f"""
INSERT DATA {{
  GRAPH <{graph_uri}> {{
{triples_nt}
  }}
}}
"""

        try:
            logger.info(f"Inserting {triple_count} triples into graph {graph_id}")
            run_sparql_query(sparql_insert, self.endpoint_url)
            logger.info(f"Successfully inserted {triple_count} triples for graph {graph_id}")
            return triple_count
        except Exception as e:
            logger.error(f"Failed to insert graph data: {e}")
            raise

    def get_graph_metadata(self, graph_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve metadata for a specific graph.

        Args:
            graph_id: Unique identifier for the graph

        Returns:
            Dictionary with graph metadata or None if not found
        """
        graph_uri = f"{GRAPE_GRAPHS}{graph_id}"

        sparql_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX grape: <http://grape.app/vocab#>

SELECT ?name ?createdAt ?updatedAt
FROM <{GRAPE_METADATA}>
WHERE {{
  <{graph_uri}> rdf:type grape:KnowledgeGraph ;
                grape:name ?name ;
                grape:createdAt ?createdAt ;
                grape:updatedAt ?updatedAt .
}}
"""

        try:
            csv_result = run_sparql_query(sparql_query, self.endpoint_url)
            lines = csv_result.strip().split('\n')
            
            if len(lines) < 2:  # No data rows
                return None
            
            # Parse CSV result
            values = lines[1].split(',')
            if len(values) >= 3:
                return {
                    "id": graph_id,
                    "name": values[0].strip(),
                    "createdAt": values[1].strip(),
                    "updatedAt": values[2].strip(),
                }
            return None
        except Exception as e:
            logger.error(f"Failed to get graph metadata: {e}")
            return None

    def list_graphs(self) -> List[Dict[str, Any]]:
        """
        List all knowledge graphs in the system.

        Returns:
            List of graph metadata dictionaries
        """
        sparql_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX grape: <http://grape.app/vocab#>

SELECT ?graph ?name ?createdAt ?updatedAt
FROM <{GRAPE_METADATA}>
WHERE {{
  ?graph rdf:type grape:KnowledgeGraph ;
         grape:name ?name ;
         grape:createdAt ?createdAt ;
         grape:updatedAt ?updatedAt .
}}
ORDER BY DESC(?createdAt)
"""

        try:
            csv_result = run_sparql_query(sparql_query, self.endpoint_url)
            lines = csv_result.strip().split('\n')
            
            graphs = []
            for line in lines[1:]:  # Skip header
                if not line.strip():
                    continue
                values = line.split(',')
                if len(values) >= 4:
                    graph_uri = values[0].strip()
                    # Extract ID from URI
                    graph_id = graph_uri.split('/')[-1]
                    graphs.append({
                        "id": graph_id,
                        "name": values[1].strip(),
                        "createdAt": values[2].strip(),
                        "updatedAt": values[3].strip(),
                    })
            
            return graphs
        except Exception as e:
            logger.error(f"Failed to list graphs: {e}")
            return []

    def delete_graph(self, graph_id: str) -> bool:
        """
        Delete a graph and its metadata.

        Args:
            graph_id: Unique identifier for the graph

        Returns:
            True if successful, False otherwise
        """
        graph_uri = f"{GRAPE_GRAPHS}{graph_id}"

        # Delete metadata
        sparql_delete_metadata = f"""
PREFIX grape: <http://grape.app/vocab#>

DELETE WHERE {{
  GRAPH <{GRAPE_METADATA}> {{
    <{graph_uri}> ?p ?o .
  }}
}}
"""

        # Delete graph data
        sparql_delete_data = f"""
DROP GRAPH <{graph_uri}>
"""

        try:
            logger.info(f"Deleting graph {graph_id}")
            # Delete metadata first
            run_sparql_query(sparql_delete_metadata, self.endpoint_url)
            # Then delete graph data
            run_sparql_query(sparql_delete_data, self.endpoint_url)
            logger.info(f"Successfully deleted graph {graph_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete graph: {e}")
            raise
