resource "helm_release" "postgres" {
  name       = "openbank-postgres"
  namespace  = var.namespace
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "postgresql"
  timeout    = 600

  set = [
    {
      name  = "auth.username"
      value = var.username
    },
    {
      name  = "auth.password"
      value = var.password
    },
    {
      name  = "auth.database"
      value = "openbank"
    },
    {
      name  = "primary.persistence.enabled"
      value = "false"
    },
  ]
}
