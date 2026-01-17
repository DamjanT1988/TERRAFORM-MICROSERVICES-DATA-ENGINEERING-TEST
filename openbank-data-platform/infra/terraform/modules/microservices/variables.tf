variable "namespace" {
  type        = string
  description = "Namespace for deployments"
}

variable "image_tag" {
  type        = string
  description = "Image tag"
}

variable "db_username" {
  type        = string
  description = "DB username"
}

variable "db_password" {
  type        = string
  description = "DB password"
  sensitive   = true
}

variable "api_key" {
  type        = string
  description = "API key"
  sensitive   = true
}
