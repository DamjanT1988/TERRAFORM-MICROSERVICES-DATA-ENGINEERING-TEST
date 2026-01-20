resource "kubernetes_deployment_v1" "ingest" {
  metadata {
    name      = "ingest"
    namespace = var.namespace
    labels = {
      app = "ingest"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "ingest"
      }
    }
    template {
      metadata {
        labels = {
          app = "ingest"
        }
      }
      spec {
        container {
          name  = "ingest"
          image = "openbank/ingest:${var.image_tag}"
          port {
            container_port = 8001
          }
          env {
            name  = "INGEST_MINIO_ENDPOINT"
            value = "openbank-minio:9000"
          }
          env {
            name  = "INGEST_MINIO_ACCESS_KEY"
            value = "minioadmin"
          }
          env {
            name  = "INGEST_MINIO_SECRET_KEY"
            value = "minioadmin"
          }
          env {
            name  = "INGEST_MINIO_BUCKET"
            value = "raw-transactions"
          }
          env {
            name  = "INGEST_RABBITMQ_URL"
            value = "amqp://guest:guest@openbank-rabbitmq:5672/"
          }
        }
      }
    }
  }
}

resource "kubernetes_service_v1" "ingest" {
  metadata {
    name      = "ingest"
    namespace = var.namespace
  }
  spec {
    selector = {
      app = "ingest"
    }
    port {
      port        = 8001
      target_port = 8001
    }
  }
}

resource "kubernetes_deployment_v1" "transform" {
  metadata {
    name      = "transform"
    namespace = var.namespace
    labels = {
      app = "transform"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "transform"
      }
    }
    template {
      metadata {
        labels = {
          app = "transform"
        }
      }
      spec {
        container {
          name    = "transform"
          image   = "openbank/transform:${var.image_tag}"
          command = ["sh", "-c"]
          args    = ["alembic upgrade head && python -m app.worker"]
          env {
            name  = "TRANSFORM_MINIO_ENDPOINT"
            value = "openbank-minio:9000"
          }
          env {
            name  = "TRANSFORM_MINIO_ACCESS_KEY"
            value = "minioadmin"
          }
          env {
            name  = "TRANSFORM_MINIO_SECRET_KEY"
            value = "minioadmin"
          }
          env {
            name  = "TRANSFORM_MINIO_BUCKET"
            value = "raw-transactions"
          }
          env {
            name  = "TRANSFORM_RABBITMQ_URL"
            value = "amqp://guest:guest@openbank-rabbitmq:5672/"
          }
          env {
            name  = "TRANSFORM_DATABASE_URL"
            value = "postgresql+psycopg2://${var.db_username}:${var.db_password}@openbank-postgres:5432/openbank"
          }
        }
      }
    }
  }
}

resource "kubernetes_deployment_v1" "api" {
  metadata {
    name      = "api"
    namespace = var.namespace
    labels = {
      app = "api"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "api"
      }
    }
    template {
      metadata {
        labels = {
          app = "api"
        }
      }
      spec {
        container {
          name  = "api"
          image = "openbank/api:${var.image_tag}"
          port {
            container_port = 8002
          }
          env {
            name  = "API_DATABASE_URL"
            value = "postgresql+psycopg2://${var.db_username}:${var.db_password}@openbank-postgres:5432/openbank"
          }
          env {
            name  = "API_API_KEY"
            value = var.api_key
          }
        }
      }
    }
  }
}

resource "kubernetes_service_v1" "api" {
  metadata {
    name      = "api"
    namespace = var.namespace
  }
  spec {
    selector = {
      app = "api"
    }
    port {
      port        = 8002
      target_port = 8002
    }
  }
}
