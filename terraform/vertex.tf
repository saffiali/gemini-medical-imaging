# Note: Deploying MedGemma or MedSigLip directly might require specific Model Garden IDs 
# or container URIs. We will use generic Vertex AI Endpoint provisioning where the models
# can be deployed once Model Garden configuration is provided.

resource "google_vertex_ai_endpoint" "medgemma_endpoint" {
  name         = "medgemma-endpoint"
  display_name = "medgemma-endpoint"
  description  = "Endpoint for MedGemma Foundation Model"
  location     = var.region
  project      = var.project_id
}

resource "google_vertex_ai_endpoint" "medsiglip_endpoint" {
  name         = "medsiglip-endpoint"
  display_name = "medsiglip-endpoint"
  description  = "Endpoint for MedSigLip Foundation Model"
  location     = var.region
  project      = var.project_id
}

# You would typically also have google_vertex_ai_model and google_vertex_ai_endpoint_model_deployment
# resources here referencing the Google Model Garden public models.
