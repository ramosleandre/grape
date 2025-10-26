"""
Ontology Context Builder Pipeline
Retrieve ontology/schema information around concepts for LLM context.
"""

from typing import List, Dict, Any, Optional
from pipelines.sparql_query_executor import SPARQLExecutor
from core.config import settings
import logging

logger = logging.getLogger(__name__)


class OntologyContextBuilder:
    """Build ontology context for concepts."""

    def __init__(self, endpoint: Optional[str] = None):
        self.executor = SPARQLExecutor(endpoint)
        self.ontology_endpoint = settings.ontologies_sparql_endpoint_url or endpoint

    async def build(
        self,
        concept_uri: str,
        include_hierarchy: bool = True,
        include_properties: bool = True,
        include_domain_range: bool = True,
    ) -> Dict[str, Any]:
        """
        Build ontology context for a concept.

        Args:
            concept_uri: URI of the concept
            include_hierarchy: Include class hierarchy
            include_properties: Include property definitions
            include_domain_range: Include domain/range constraints

        Returns:
            Ontology context dictionary
        """
        context = {
            "concept": concept_uri,
            "hierarchy": {},
            "properties": [],
            "constraints": {},
        }

        if include_hierarchy:
            context["hierarchy"] = await self._get_hierarchy(concept_uri)

        if include_properties:
            context["properties"] = await self._get_properties(concept_uri)

        if include_domain_range:
            context["constraints"] = await self._get_domain_range(concept_uri)

        return context

    async def _get_hierarchy(self, concept_uri: str) -> Dict[str, List[str]]:
        """Get class hierarchy (superclasses and subclasses)."""
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT ?superClass ?subClass ?superLabel ?subLabel WHERE {{
            {{
                <{concept_uri}> rdfs:subClassOf ?superClass .
                OPTIONAL {{ ?superClass rdfs:label ?superLabel }}
            }}
            UNION
            {{
                ?subClass rdfs:subClassOf <{concept_uri}> .
                OPTIONAL {{ ?subClass rdfs:label ?subLabel }}
            }}
        }}
        LIMIT 100
        """

        try:
            results = await self.executor.execute(query)

            superclasses = []
            subclasses = []

            for r in results:
                if r.get("superClass"):
                    superclasses.append({
                        "uri": r["superClass"],
                        "label": r.get("superLabel", r["superClass"].split("/")[-1])
                    })
                if r.get("subClass"):
                    subclasses.append({
                        "uri": r["subClass"],
                        "label": r.get("subLabel", r["subClass"].split("/")[-1])
                    })

            return {
                "superclasses": superclasses,
                "subclasses": subclasses,
            }

        except Exception as e:
            logger.error(f"Failed to get hierarchy: {e}")
            return {"superclasses": [], "subclasses": []}

    async def _get_properties(self, concept_uri: str) -> List[Dict[str, Any]]:
        """Get properties associated with the concept."""
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT DISTINCT ?property ?propertyLabel ?propertyType WHERE {{
            {{
                ?property rdfs:domain <{concept_uri}> .
            }}
            UNION
            {{
                ?property rdfs:range <{concept_uri}> .
            }}
            OPTIONAL {{ ?property rdfs:label ?propertyLabel }}
            OPTIONAL {{ ?property a ?propertyType }}
        }}
        LIMIT 100
        """

        try:
            results = await self.executor.execute(query)

            properties = []
            for r in results:
                properties.append({
                    "uri": r["property"],
                    "label": r.get("propertyLabel", r["property"].split("/")[-1]),
                    "type": r.get("propertyType", "rdf:Property"),
                })

            return properties

        except Exception as e:
            logger.error(f"Failed to get properties: {e}")
            return []

    async def _get_domain_range(self, concept_uri: str) -> Dict[str, Any]:
        """Get domain and range constraints."""
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT ?property ?domain ?range ?domainLabel ?rangeLabel WHERE {{
            {{
                ?property rdfs:domain <{concept_uri}> .
                OPTIONAL {{ ?property rdfs:range ?range }}
                OPTIONAL {{ ?range rdfs:label ?rangeLabel }}
            }}
            UNION
            {{
                ?property rdfs:range <{concept_uri}> .
                OPTIONAL {{ ?property rdfs:domain ?domain }}
                OPTIONAL {{ ?domain rdfs:label ?domainLabel }}
            }}
        }}
        LIMIT 100
        """

        try:
            results = await self.executor.execute(query)

            constraints = []
            for r in results:
                constraint = {
                    "property": r["property"],
                }
                if r.get("domain"):
                    constraint["domain"] = {
                        "uri": r["domain"],
                        "label": r.get("domainLabel", r["domain"].split("/")[-1])
                    }
                if r.get("range"):
                    constraint["range"] = {
                        "uri": r["range"],
                        "label": r.get("rangeLabel", r["range"].split("/")[-1])
                    }
                constraints.append(constraint)

            return {"constraints": constraints}

        except Exception as e:
            logger.error(f"Failed to get domain/range: {e}")
            return {"constraints": []}

    async def build_schema_summary(self, limit: int = 50) -> Dict[str, Any]:
        """
        Get high-level schema summary of the KG.

        Returns:
            Summary with main classes and properties
        """
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT DISTINCT ?class ?label (COUNT(?instance) as ?instanceCount) WHERE {{
            ?class a owl:Class .
            OPTIONAL {{ ?class rdfs:label ?label }}
            OPTIONAL {{ ?instance a ?class }}
        }}
        GROUP BY ?class ?label
        ORDER BY DESC(?instanceCount)
        LIMIT {limit}
        """

        try:
            results = await self.executor.execute(query)

            classes = []
            for r in results:
                classes.append({
                    "uri": r["class"],
                    "label": r.get("label", r["class"].split("/")[-1]),
                    "instance_count": int(r.get("instanceCount", 0)),
                })

            return {"classes": classes}

        except Exception as e:
            logger.error(f"Failed to get schema summary: {e}")
            return {"classes": []}
