provider "kubernetes" {
  config_path = var.kubeconfig_path
}

provider "helm" {
  kubernetes = {
    config_path = var.kubeconfig_path
  }
}

module "k8s_base" {
  source      = "../../modules/k8s-base"
  namespace   = var.namespace
  db_username = var.db_username
  db_password = var.db_password
  api_key     = var.api_key
}

module "postgres" {
  source    = "../../modules/helm-postgres"
  namespace = var.namespace
  username  = var.db_username
  password  = var.db_password
}

module "minio" {
  source    = "../../modules/helm-minio"
  namespace = var.namespace
}

module "rabbitmq" {
  source    = "../../modules/helm-rabbitmq"
  namespace = var.namespace
}

module "microservices" {
  source      = "../../modules/microservices"
  namespace   = var.namespace
  image_tag   = var.image_tag
  db_username = var.db_username
  db_password = var.db_password
  api_key     = var.api_key
  depends_on  = [module.postgres, module.minio, module.rabbitmq]
}
