resource "helm_release" "minio" {
  name       = "openbank-minio"
  namespace  = var.namespace
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "minio"
  version    = "14.8.2"

  set = [
    {
      name  = "auth.rootUser"
      value = "minioadmin"
    },
    {
      name  = "auth.rootPassword"
      value = "minioadmin"
    },
    {
      name  = "persistence.enabled"
      value = "false"
    },
  ]
}
