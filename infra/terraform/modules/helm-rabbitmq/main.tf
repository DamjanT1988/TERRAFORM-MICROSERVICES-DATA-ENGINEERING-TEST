resource "kubernetes_deployment_v1" "rabbitmq" {
  metadata {
    name      = "openbank-rabbitmq"
    namespace = var.namespace
    labels = {
      app = "openbank-rabbitmq"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "openbank-rabbitmq"
      }
    }
    template {
      metadata {
        labels = {
          app = "openbank-rabbitmq"
        }
      }
      spec {
        container {
          name  = "rabbitmq"
          image = "rabbitmq:3.13-management"
          port {
            container_port = 5672
          }
          port {
            container_port = 15672
          }

          env {
            name  = "RABBITMQ_DEFAULT_USER"
            value = "guest"
          }
          env {
            name  = "RABBITMQ_DEFAULT_PASS"
            value = "guest"
          }

          volume_mount {
            name       = "data"
            mount_path = "/var/lib/rabbitmq"
          }
        }

        volume {
          name = "data"
          empty_dir {}
        }
      }
    }
  }
}

resource "kubernetes_service_v1" "rabbitmq" {
  metadata {
    name      = "openbank-rabbitmq"
    namespace = var.namespace
  }
  spec {
    selector = {
      app = "openbank-rabbitmq"
    }
    port {
      name        = "amqp"
      port        = 5672
      target_port = 5672
    }
    port {
      name        = "management"
      port        = 15672
      target_port = 15672
    }
  }
}
