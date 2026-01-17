variable "kubeconfig_path" {
  type        = string
  description = "Path to kubeconfig for local kind/k3d cluster"
  default     = "~/.kube/config"
}

variable "namespace" {
  type        = string
  description = "Kubernetes namespace for the platform"
  default     = "openbank"
}

variable "db_username" {
  type        = string
  description = "PostgreSQL username"
  default     = "postgres"
}

variable "db_password" {
  type        = string
  description = "PostgreSQL password"
  default     = "postgres"
  sensitive   = true
}

variable "api_key" {
  type        = string
  description = "API key for api-service"
  default     = "local-dev-key"
  sensitive   = true
}

variable "image_tag" {
  type        = string
  description = "Local image tag"
  default     = "local"
}
