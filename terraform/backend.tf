# Backend (remote state) for Terraform
# NOTE: backend config values cannot use variables inside the block. We therefore
# recommend supplying backend configuration at `terraform init` using
# -backend-config flags. Example:
#
# terraform init \
#   -backend-config="bucket=grape-terraform-state-<YOUR_BUCKET>" \
#   -backend-config="prefix=dev/terraform.tfstate"
#
terraform {
  backend "gcs" {
    # Example partial config (commented). Replace or provide -backend-config at init.
    # bucket = "grape-terraform-state-<YOUR_BUCKET>"
    # prefix = "${var.env}/terraform.tfstate"  # cannot use var in backend block — provide at init
  }
}
