resource "kubernetes_namespace_v1" "this" {
  metadata {
    name = var.namespace
  }
}

resource "kubernetes_secret_v1" "db" {
  metadata {
    name      = "openbank-db"
    namespace = kubernetes_namespace_v1.this.metadata[0].name
  }

  data = {
    username = var.db_username
    password = var.db_password
  }

  type = "Opaque"
}

resource "kubernetes_secret_v1" "api" {
  metadata {
    name      = "openbank-api"
    namespace = kubernetes_namespace_v1.this.metadata[0].name
  }

  data = {
    api_key = var.api_key
  }

  type = "Opaque"
}
