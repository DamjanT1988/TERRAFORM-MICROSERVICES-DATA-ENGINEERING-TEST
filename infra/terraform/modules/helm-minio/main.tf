resource "kubernetes_deployment_v1" "minio" {
  metadata {
    name      = "openbank-minio"
    namespace = var.namespace
    labels = {
      app = "openbank-minio"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "openbank-minio"
      }
    }
    template {
      metadata {
        labels = {
          app = "openbank-minio"
        }
      }
      spec {
        container {
          name  = "minio"
          image = "minio/minio:RELEASE.2024-08-17T01-24-54Z"
          args  = ["server", "/data", "--console-address", ":9001"]

          port {
            container_port = 9000
          }
          port {
            container_port = 9001
          }

          env {
            name  = "MINIO_ROOT_USER"
            value = "minioadmin"
          }
          env {
            name  = "MINIO_ROOT_PASSWORD"
            value = "minioadmin"
          }

          volume_mount {
            name       = "data"
            mount_path = "/data"
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

resource "kubernetes_service_v1" "minio" {
  metadata {
    name      = "openbank-minio"
    namespace = var.namespace
  }
  spec {
    selector = {
      app = "openbank-minio"
    }
    port {
      name        = "api"
      port        = 9000
      target_port = 9000
    }
    port {
      name        = "console"
      port        = 9001
      target_port = 9001
    }
  }
}
