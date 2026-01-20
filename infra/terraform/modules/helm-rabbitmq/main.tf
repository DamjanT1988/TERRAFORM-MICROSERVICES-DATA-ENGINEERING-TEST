resource "helm_release" "rabbitmq" {
  name       = "openbank-rabbitmq"
  namespace  = var.namespace
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "rabbitmq"
  version    = "15.1.5"

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
  ]
}
