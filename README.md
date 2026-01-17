# OpenBank Data Platform

A cloud-ready, containerized data engineering platform for financial transaction data. Raw banking transaction data is ingested, validated, transformed into curated datasets, stored in PostgreSQL, and exposed via APIs. The platform runs locally on Kubernetes and is fully provisioned using Terraform, with an Azure-ready infrastructure layer.

This is a portofolio project developed by Damjan with assistance of Co-Pilot. The aim is to learn relevant skills for data engineering and develop skills in microservices, infrastructure as code, and cloud.

## Problem Statement

Financial teams need reliable, traceable pipelines for ingesting and curating raw transaction data while preserving auditability, flagging anomalies, and providing secure read-only access for analytics and downstream systems.

## Architecture

```
                +-------------------+
CSV / JSON ---> | ingest-service    | ----> MinIO (raw objects)
                | FastAPI           |         |
                +-------------------+         |
                          |                   |
                          v                   |
                    Message Broker            |
                          |                   |
                          v                   |
                +-------------------+         |
                | transform-service | <-------+
                | Python worker     |
                +-------------------+
                     |         |
                     v         v
          raw_transactions   curated_transactions
                 (PostgreSQL 15+)
                     |
                     v
                +-------------------+
                | api-service       |
                | FastAPI + API key |
                +-------------------+
```

## Tech Stack

- Python 3.11, FastAPI, Pydantic, SQLAlchemy, Alembic
- PostgreSQL 15+
- MinIO (S3-compatible object storage)
- RabbitMQ (message broker)
- Docker + Docker Compose
- Kubernetes (kind/k3d) + Terraform
- Azure-ready Terraform (AKS, ACR, PostgreSQL Flexible Server, Key Vault)
- CI/CD with GitHub Actions (ruff, black, pytest, terraform)

## Local Setup (Docker Compose)

1. Build and start:
   - `docker compose up --build`
2. Services:
   - `ingest-service` on `http://localhost:8001`
   - `api-service` on `http://localhost:8002`
3. Example ingestion:
   - Upload CSV: `POST /ingest/csv`
   - JSON POST: `POST /ingest/json`
4. Sample data:
   - `data/transactions_raw.csv`
5. API auth:
   - Send `x-api-key: local-dev-key` in request headers

## Local Kubernetes via Terraform

The local Terraform environment:

- Creates namespaces and secrets
- Deploys PostgreSQL, MinIO, RabbitMQ
- Deploys all services

Steps:

1. Create a local cluster (kind or k3d).
2. Build images and load into the cluster:
   - `docker build -t openbank/ingest:local services/ingest`
   - `docker build -t openbank/transform:local services/transform`
   - `docker build -t openbank/api:local services/api`
   - `kind load docker-image openbank/ingest:local openbank/transform:local openbank/api:local`
3. `cd infra/terraform/envs/local-kind`
4. `terraform init`
5. `terraform apply`

## Testing Strategy

- Unit tests:
  - Validation logic (schema checks)
  - Transformation logic (dedupe, flags)
  - Repository layer (SQLAlchemy models)
- Integration tests:
  - Spin up Postgres, MinIO, RabbitMQ
  - Run ingest -> transform -> API flow

## CI/CD Overview

GitHub Actions workflows run:

- Linting with `ruff`
- Formatting with `black`
- Unit tests with `pytest`
- Integration tests with Docker services
- Docker image builds
- Terraform `fmt` and `validate`

## Terraform Structure

```
infra/terraform/
  modules/
    aks/
    acr/
    helm-minio/
    helm-postgres/
    helm-rabbitmq/
    postgres/
    keyvault/
    k8s-base/
    microservices/
  envs/
    local-kind/
    azure/
```

## Azure Cloud-Ready

The Azure environment is provided as a documented, modular Terraform setup:

- Resource Group
- ACR for container images
- AKS for Kubernetes
- PostgreSQL Flexible Server
- Key Vault for secrets

This is intended as a cloud-ready blueprint and may require Azure credentials and quota to apply.

## Future Improvements

- Add CDC ingestion and incremental loads
- Implement data lineage and catalog (OpenMetadata)
- Add RBAC and OAuth2
- Expand anomaly detection rules
- Add Airflow or Dagster orchestration
