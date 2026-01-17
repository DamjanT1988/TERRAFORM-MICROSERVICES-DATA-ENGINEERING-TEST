resource "azurerm_postgresql_flexible_server" "this" {
  name                   = var.name
  resource_group_name    = var.resource_group_name
  location               = var.location
  version                = "15"
  administrator_login    = var.admin_username
  administrator_password = var.admin_password
  sku_name               = "B_Standard_B1ms"
  storage_mb             = 32768
}

resource "azurerm_postgresql_flexible_server_database" "openbank" {
  name      = "openbank"
  server_id = azurerm_postgresql_flexible_server.this.id
}
