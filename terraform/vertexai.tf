// Vertex AI: API was enabled in main.tf. Additional roles for service accounts can be assigned here.
resource "google_project_iam_member" "backend_aiplatform_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.backend_sa.email}"
}
