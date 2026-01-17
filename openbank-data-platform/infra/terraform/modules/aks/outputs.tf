output "name" {
  value = azurerm_kubernetes_cluster.this.name
}

output "tenant_id" {
  value = azurerm_kubernetes_cluster.this.identity[0].tenant_id
}
