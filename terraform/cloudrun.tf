resource "google_artifact_registry_repository" "app_repo" {
  location      = var.region
  repository_id = "${var.app_name}-repo"
  description   = "Docker repository for Medical Imaging PoV App"
  format        = "DOCKER"
  project       = var.project_id
}

# We define the service, but the initial image will be a placeholder or the deployment 
# will be done via gcloud/Cloud Build after terraform apply.
resource "google_cloud_run_v2_service" "app_service" {
  name     = "${var.app_name}-service"
  location = var.region
  project  = var.project_id
  
  template {
    service_account = google_service_account.app_sa.email
    containers {
      # Use a placeholder image until the real app is built
      image = "us-docker.pkg.dev/cloudrun/container/hello" 
      
      env {
        name  = "PROJECT_ID"
        value = var.project_id
      }
      env {
        name  = "REGION"
        value = var.region
      }
      env {
        name  = "WSI_BUCKET"
        value = google_storage_bucket.wsi_images.name
      }
      env {
        name  = "MASKS_BUCKET"
        value = google_storage_bucket.masks_output.name
      }
      env {
        name  = "REPORTS_BUCKET"
        value = google_storage_bucket.reports_output.name
      }
      env {
        name  = "MEDGEMMA_ENDPOINT"
        value = google_vertex_ai_endpoint.medgemma_endpoint.id
      }
      env {
        name  = "MEDSIGLIP_ENDPOINT"
        value = google_vertex_ai_endpoint.medsiglip_endpoint.id
      }
    }
  }
  
  lifecycle {
    ignore_changes = [
      template[0].containers[0].image,
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth_policy" {
  location    = google_cloud_run_v2_service.app_service.location
  project     = google_cloud_run_v2_service.app_service.project
  service     = google_cloud_run_v2_service.app_service.name

  policy_data = data.google_iam_policy.noauth.policy_data
}
