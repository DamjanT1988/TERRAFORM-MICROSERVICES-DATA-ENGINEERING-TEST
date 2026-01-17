variable "namespace" {
  type        = string
  description = "Namespace name"
}

variable "db_username" {
  type        = string
  description = "Database user"
}

variable "db_password" {
  type        = string
  description = "Database password"
  sensitive   = true
}

variable "api_key" {
  type        = string
  description = "API key for api-service"
  sensitive   = true
}
