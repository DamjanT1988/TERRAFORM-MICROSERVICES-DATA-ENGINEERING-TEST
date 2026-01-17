resource "helm_release" "postgres" {
  name       = "openbank-postgres"
  namespace  = var.namespace
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "postgresql"
  version    = "15.5.1"

  set {
    name  = "auth.username"
    value = var.username
  }
  set {
    name  = "auth.password"
    value = var.password
  }
  set {
    name  = "auth.database"
    value = "openbank"
  }
  set {
    name  = "primary.persistence.enabled"
    value = "false"
  }
}
