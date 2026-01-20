resource "helm_release" "minio" {
  name       = "openbank-minio"
  namespace  = var.namespace
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "minio"
  timeout    = 600

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
    {
      name  = "image.tag"
      value = "latest"
    },
    {
      name  = "consoleImage.tag"
      value = "latest"
    },
  ]
}
