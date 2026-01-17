variable "namespace" {
  type        = string
  description = "Namespace for PostgreSQL"
}

variable "username" {
  type        = string
  description = "PostgreSQL username"
}

variable "password" {
  type        = string
  description = "PostgreSQL password"
  sensitive   = true
}
