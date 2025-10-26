// Create secrets (no versions/values stored here). Add versions via gcloud or CI.
resource "google_secret_manager_secret" "graphdb_uri" {
  project = var.project_id
  secret_id = "graphdb_uri-${var.env}"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret" "graphdb_user" {
  project = var.project_id
  secret_id = "graphdb_user-${var.env}"
  replication { automatic = true }
}

resource "google_secret_manager_secret" "graphdb_password" {
  project = var.project_id
  secret_id = "graphdb_password-${var.env}"
  replication { automatic = true }
}

resource "google_secret_manager_secret" "vertex_api_key" {
  project = var.project_id
  secret_id = "vertex_api_key-${var.env}"
  replication { automatic = true }
}

// Grant access to backend service account to read secrets
resource "google_secret_manager_secret_iam_member" "graphdb_uri_access" {
  secret_id = google_secret_manager_secret.graphdb_uri.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.backend_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "graphdb_user_access" {
  secret_id = google_secret_manager_secret.graphdb_user.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.backend_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "graphdb_password_access" {
  secret_id = google_secret_manager_secret.graphdb_password.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.backend_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "vertex_api_key_access" {
  secret_id = google_secret_manager_secret.vertex_api_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.backend_sa.email}"
}
