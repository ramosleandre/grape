resource "google_artifact_registry_repository" "docker_repo" {
  provider = google
  project  = var.project_id
  location = var.artifact_registry_location
  repository_id = var.artifact_repo_name
  format = "DOCKER"
  description = "Private Docker repository for Grape backend images"
}

// IAM bindings for the repository will be granted to service accounts in iam.tf
