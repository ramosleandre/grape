// Service accounts
resource "google_service_account" "backend_sa" {
  account_id   = "grape-backend-${var.env}"
  display_name = "Grape backend service account (${var.env})"
  project      = var.project_id
}

resource "google_service_account" "deployer_sa" {
  account_id   = "grape-deployer-${var.env}"
  display_name = "Grape deployer service account (${var.env})"
  project      = var.project_id
}

// Minimal roles for backend service account
resource "google_project_iam_member" "backend_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${google_service_account.backend_sa.email}"
}

resource "google_project_iam_member" "backend_secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.backend_sa.email}"
}

resource "google_project_iam_member" "backend_artifact_reader" {
  project = var.project_id
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.backend_sa.email}"
}

resource "google_project_iam_member" "deployer_artifact_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.deployer_sa.email}"
}

resource "google_project_iam_member" "logging_writer_backend" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.backend_sa.email}"
}

// Vertex AI user role for backend when interacting with Vertex
resource "google_project_iam_member" "backend_vertex_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.backend_sa.email}"
}

// Grant deployer minimal roles for Cloud Run deploy & Artifact Registry write
resource "google_project_iam_member" "deployer_run_deployer" {
  project = var.project_id
  role    = "roles/run.developer"
  member  = "serviceAccount:${google_service_account.deployer_sa.email}"
}
