// Placeholder for Graph DB (Neo4j Aura) integration.
// Many managed Graph DB offerings (Neo4j Aura) are not fully provisionable via the
// hashicorp/google provider. If an official provider exists for Neo4j Aura, add it here.

// For now, we create a local placeholder resource and instruct how to add credentials
// to Secret Manager. If you have a managed instance created manually, store its
// connection string and credentials into the Secret Manager secrets created in secretmanager.tf.

resource "null_resource" "graphdb_placeholder" {
  triggers = {
    env = var.env
  }
}

// Document manual steps in README: create Neo4j Aura instance in GCP marketplace or Neo4j console,
// then store connection URI, user and password into secrets:
// - projects/PROJECT_ID/secrets/graphdb_uri-<env>
// - projects/PROJECT_ID/secrets/graphdb_user-<env>
// - projects/PROJECT_ID/secrets/graphdb_password-<env>
