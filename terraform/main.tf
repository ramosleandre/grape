// Activate required Google APIs
resource "google_project_service" "cloudrun" {
  service = "run.googleapis.com"
  project = var.project_id
}

resource "google_project_service" "artifactregistry" {
  service = "artifactregistry.googleapis.com"
  project = var.project_id
}

resource "google_project_service" "secretmanager" {
  service = "secretmanager.googleapis.com"
  project = var.project_id
}

resource "google_project_service" "vertexai" {
  service = "vertexai.googleapis.com"
  project = var.project_id
}

resource "google_project_service" "firebase" {
  service = "firebase.googleapis.com"
  project = var.project_id
}

resource "google_project_service" "servicenetworking" {
  service = "servicenetworking.googleapis.com"
  project = var.project_id
}

resource "google_project_service" "compute" {
  service = "compute.googleapis.com"
  project = var.project_id
}

// Ensure other APIs used by Cloud Run & monitoring
resource "google_project_service" "cloudbuild" {
  service = "cloudbuild.googleapis.com"
  project = var.project_id
}

resource "google_project_service" "logging" {
  service = "logging.googleapis.com"
  project = var.project_id
}
