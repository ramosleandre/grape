// Link Firebase to the existing GCP project
resource "google_firebase_project" "project" {
  project = var.project_id
}

// Note: Terraform's Firebase provider may not manage Hosting sites completely.
// We create the Firebase project resource; final hosting setup (site deploy) is documented in README.
