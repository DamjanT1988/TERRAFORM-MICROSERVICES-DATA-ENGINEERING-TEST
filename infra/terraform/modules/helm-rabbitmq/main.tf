resource "helm_release" "rabbitmq" {
  name       = "openbank-rabbitmq"
  namespace  = var.namespace
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "rabbitmq"
  timeout    = 600

  set = [
    {
      name  = "auth.username"
      value = "guest"
    },
    {
      name  = "auth.password"
      value = "guest"
    },
    {
      name  = "persistence.enabled"
      value = "false"
    },
    {
      name  = "image.tag"
      value = "latest"
    },
  ]
}
