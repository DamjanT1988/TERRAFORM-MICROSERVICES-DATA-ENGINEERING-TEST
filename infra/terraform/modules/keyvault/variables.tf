variable "name" {
  type        = string
  description = "Key Vault name"
}

variable "resource_group_name" {
  type        = string
  description = "Resource group"
}

variable "location" {
  type        = string
  description = "Azure region"
}

variable "tenant_id" {
  type        = string
  description = "Azure tenant ID"
}
