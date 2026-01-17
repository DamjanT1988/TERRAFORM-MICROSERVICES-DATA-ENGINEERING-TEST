variable "name" {
  type        = string
  description = "PostgreSQL Flexible Server name"
}

variable "resource_group_name" {
  type        = string
  description = "Resource group"
}

variable "location" {
  type        = string
  description = "Azure region"
}

variable "admin_username" {
  type        = string
  description = "PostgreSQL admin username"
}

variable "admin_password" {
  type        = string
  description = "PostgreSQL admin password"
  sensitive   = true
}
