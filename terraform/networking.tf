resource "google_compute_network" "vpc" {
  name                    = var.vpc_name
  project                 = var.project_id
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "${var.vpc_name}-${var.env}-subnet"
  ip_cidr_range = "10.10.${lookup({dev=10,staging=20,prod=30}, var.env, 50)}.0/24"
  region        = var.region
  network       = google_compute_network.vpc.id
  project       = var.project_id
}

resource "google_compute_firewall" "allow-egress" {
  name    = "${var.vpc_name}-${var.env}-allow-egress"
  network = google_compute_network.vpc.name
  project = var.project_id
  direction = "EGRESS"
  priority  = 1000
  allow {
    protocol = "all"
  }
  destination_ranges = ["0.0.0.0/0"]
}

// Restrictive management ingress rule (if allowed_cidrs narrower than 0.0.0.0/0)
resource "google_compute_firewall" "management-ingress" {
  name    = "${var.vpc_name}-${var.env}-management-ingress"
  network = google_compute_network.vpc.name
  project = var.project_id
  direction = "INGRESS"
  priority  = 1000
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  source_ranges = var.allowed_cidrs
}
