resource "google_cloud_run_service" "backend" {
  name     = "grape-backend-${var.env}"
  location = var.region
  project  = var.project_id

  template {
    spec {
      service_account_name = google_service_account.backend_sa.email
      containers {
        image = var.service_image
        env {
          name = "ENV"
          value = var.env
        }
        // Sensitive envs should be provided via Secret Manager mounted or consumed by application using SDK
      }
    }
  }

  traffics {
    percent         = 100
    latest_revision = true
  }

  ingress = var.cloudrun_ingress
}

// Allow unauthenticated invocation if ingress ANY and public
resource "google_cloud_run_service_iam_member" "invoker_any" {
  service = google_cloud_run_service.backend.name
  location = google_cloud_run_service.backend.location
  project = var.project_id
  role = "roles/run.invoker"
  member = "allUsers"

  depends_on = [google_cloud_run_service.backend]
  count = var.cloudrun_ingress == "ANY" ? 1 : 0
}
