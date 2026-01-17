variable "location" {
  type        = string
  description = "Azure region"
  default     = "westeurope"
}

variable "resource_group_name" {
  type        = string
  description = "Resource group name"
  default     = "rg-openbank-data-platform"
}

variable "aks_name" {
  type        = string
  description = "AKS cluster name"
  default     = "aks-openbank"
}

variable "acr_name" {
  type        = string
  description = "ACR name (globally unique)"
  default     = "acropenbankdemo"
}

variable "postgres_name" {
  type        = string
  description = "PostgreSQL Flexible Server name"
  default     = "pg-openbank"
}

variable "postgres_admin_username" {
  type        = string
  description = "PostgreSQL admin username"
  default     = "pgadmin"
}

variable "postgres_admin_password" {
  type        = string
  description = "PostgreSQL admin password"
  default     = "ChangeMe123!"
  sensitive   = true
}

variable "keyvault_name" {
  type        = string
  description = "Key Vault name"
  default     = "kv-openbank"
}
