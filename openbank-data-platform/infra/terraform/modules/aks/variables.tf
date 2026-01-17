variable "name" {
  type        = string
  description = "AKS cluster name"
}

variable "resource_group_name" {
  type        = string
  description = "Resource group"
}

variable "location" {
  type        = string
  description = "Azure region"
}

variable "acr_id" {
  type        = string
  description = "ACR resource ID"
}
