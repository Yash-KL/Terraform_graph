variable "project_id" {
  description = "GCP project id"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "GCP zone for resources"
  type        = string
  default     = "us-central1-a"
}

variable "instance_name" {
  description = "Name for the compute instance"
  type        = string
  default     = "terraform-vm"
}

variable "machine_type" {
  description = "Machine type for the compute instance"
  type        = string
  default     = "e2-medium"
}

variable "image_project" {
  description = "Image project for the boot disk"
  type        = string
  default     = "debian-cloud"
}

variable "image_family" {
  description = "Image family to use for the boot disk"
  type        = string
  default     = "debian-11"
}
