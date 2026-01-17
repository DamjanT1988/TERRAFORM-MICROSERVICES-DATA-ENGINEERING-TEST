output "resource_group_name" {
  value = module.rg.name
}

output "aks_name" {
  value = module.aks.name
}

output "acr_login_server" {
  value = module.acr.login_server
}

output "postgres_fqdn" {
  value = module.postgres.fqdn
}

output "keyvault_uri" {
  value = module.keyvault.uri
}
