# Storage for raw WSI images
resource "google_storage_bucket" "wsi_images" {
  name                        = "${var.project_id}-${var.app_name}-wsi-images"
  location                    = var.region
  force_destroy               = false
  uniform_bucket_level_access = true

  cors {
    origin          = ["*"]
    method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
    response_header = ["*"]
    max_age_seconds = 3600
  }
}

# Storage for generated masks and tile outputs
resource "google_storage_bucket" "masks_output" {
  name                        = "${var.project_id}-${var.app_name}-masks"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}

# Storage for IOU reports
resource "google_storage_bucket" "reports_output" {
  name                        = "${var.project_id}-${var.app_name}-reports"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}
