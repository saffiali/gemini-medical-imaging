variable "project_id" {
  description = "The GCP Project ID"
  type        = string
  default     = "gsk-cmc-hackathon"
}

variable "region" {
  description = "The GCP region to deploy resources to"
  type        = string
  default     = "us-central1"
}

variable "app_name" {
  description = "Name of the application"
  type        = string
  default     = "med-imaging-pov"
}
