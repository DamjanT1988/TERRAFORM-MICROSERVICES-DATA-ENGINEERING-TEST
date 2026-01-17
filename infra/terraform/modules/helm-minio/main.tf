resource "helm_release" "minio" {
  name       = "openbank-minio"
  namespace  = var.namespace
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "minio"
  version    = "14.8.2"

  set {
    name  = "auth.rootUser"
    value = "minioadmin"
  }
  set {
    name  = "auth.rootPassword"
    value = "minioadmin"
  }
  set {
    name  = "persistence.enabled"
    value = "false"
  }
}
