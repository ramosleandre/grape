// Placeholder for RDF Triplestore (GraphDB) integration.
// GraphDB can be deployed on GCP using Compute Engine or Google Kubernetes Engine (GKE).
// This file provides a placeholder resource. The actual deployment can be done via:
// 1. GraphDB Docker container on Compute Engine VM
// 2. GraphDB Helm chart on GKE
// 3. Manual GraphDB installation and configuration

// For now, we create a local placeholder resource and instruct how to add credentials
// to Secret Manager. If you have a GraphDB instance deployed, store its
// SPARQL endpoint URL and credentials into the Secret Manager secrets created in secretmanager.tf.

resource "null_resource" "graphdb_placeholder" {
  triggers = {
    env = var.env
  }
}

// Document manual steps in README:
// Option 1: Deploy GraphDB on Compute Engine
//   - Create a VM instance with Docker
//   - Run GraphDB container: docker run -d -p 7200:7200 ontotext/graphdb:latest
//   - Access GraphDB at http://VM_IP:7200
//
// Option 2: Deploy GraphDB on GKE using Helm
//   - Install GraphDB Helm chart on your GKE cluster
//   - Configure persistent volumes and ingress
//
// Option 3: Use public SPARQL endpoints for testing
//   - DBpedia: https://dbpedia.org/sparql
//   - Wikidata: https://query.wikidata.org/sparql
//
// Then store connection details into secrets:
// - projects/PROJECT_ID/secrets/sparql_endpoint_url-<env>
// - projects/PROJECT_ID/secrets/graphdb_user-<env>
// - projects/PROJECT_ID/secrets/graphdb_password-<env>
