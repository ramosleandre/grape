variable "project_id" {
  description = "GCP project id to deploy into"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "europe-west1"
}

variable "env" {
  description = "Environment name (dev|staging|prod)"
  type        = string
}

variable "service_image" {
  description = "Container image for backend Cloud Run (full image path in Artifact Registry or GCR)"
  type        = string
  default     = ""
}

variable "artifact_repo_name" {
  description = "Artifact Registry repository name"
  type        = string
  default     = "grape-backend-repo"
}

variable "vpc_name" {
  description = "VPC name to use/create"
  type        = string
  default     = "grape-vpc"
}

variable "allowed_cidrs" {
  description = "List of CIDRs allowed for ingress (management). Cloud Run default is public HTTP(S) unless set internal." 
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "cloudrun_ingress" {
  description = "Cloud Run ingress setting: ANY, INTERNAL_ONLY, INTERNAL_AND_GCLB"
  type        = string
  default     = "ANY"
}

variable "backend_service_account" {
  description = "Email of backend service account. If empty, created automatically"
  type        = string
  default     = ""
}

variable "deployer_service_account" {
  description = "Email for deployer service account. If empty, created automatically"
  type        = string
  default     = ""
}

variable "artifact_registry_location" {
  description = "Region for Artifact Registry"
  type        = string
  default     = "europe-west1"
}

variable "state_bucket" {
  description = "(Optional) GCS bucket used for terraform remote state if baked into config"
  type        = string
  default     = ""
}
