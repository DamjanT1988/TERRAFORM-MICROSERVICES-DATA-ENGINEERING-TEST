provider "azurerm" {
  features {}
}

module "rg" {
  source   = "../../modules/rg"
  name     = var.resource_group_name
  location = var.location
}

module "acr" {
  source              = "../../modules/acr"
  name                = var.acr_name
  resource_group_name = module.rg.name
  location            = module.rg.location
}

module "aks" {
  source              = "../../modules/aks"
  name                = var.aks_name
  resource_group_name = module.rg.name
  location            = module.rg.location
  acr_id              = module.acr.id
}

module "postgres" {
  source              = "../../modules/postgres"
  name                = var.postgres_name
  resource_group_name = module.rg.name
  location            = module.rg.location
  admin_username      = var.postgres_admin_username
  admin_password      = var.postgres_admin_password
}

module "keyvault" {
  source              = "../../modules/keyvault"
  name                = var.keyvault_name
  resource_group_name = module.rg.name
  location            = module.rg.location
  tenant_id           = module.aks.tenant_id
}
