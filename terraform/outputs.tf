output "cloud_run_url" {
  value = google_cloud_run_service.backend.status[0].url
  description = "URL of the deployed Cloud Run service"
}

output "artifact_repo_url" {
  value = "${var.artifact_registry_location}-docker.pkg.dev/${var.project_id}/${var.artifact_repo_name}"
  description = "Artifact Registry docker repository URL prefix"
}

output "firebase_project" {
  value = google_firebase_project.project.project
  description = "Firebase project id"
}

output "secret_names" {
  value = [
    google_secret_manager_secret.graphdb_uri.secret_id,
    google_secret_manager_secret.graphdb_user.secret_id,
    google_secret_manager_secret.graphdb_password.secret_id,
    google_secret_manager_secret.vertex_api_key.secret_id,
  ]
}

output "backend_service_account_email" {
  value = google_service_account.backend_sa.email
}
