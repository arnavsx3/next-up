# NextUp

A simple queue management application built as a hands-on Kubernetes, Helm, autoscaling, and load-testing project.

## Architecture

React + Vite → FastAPI → Neon PostgreSQL

Kubernetes:
NGINX Ingress → Frontend / Backend
HPA → Pod autoscaling
k6 → Load testing

## Tech Stack

- Frontend: React, Vite
- Backend: Python, FastAPI, uv
- Database: Neon PostgreSQL
- ORM: SQLAlchemy
- Containerization: Docker, Docker Compose
- Kubernetes: Kubernetes, Kind, kubectl
- Packaging: Helm
- Ingress: NGINX Ingress Controller
- Autoscaling: HPA
- Metrics: Kubernetes Metrics Server
- Load Testing: k6

## Prerequisites

Install:

- Docker
- Kind
- kubectl
- Helm
- Python
- uv
- Node.js + npm
- k6

## Dependencies

### Backend

- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL driver
- python-dotenv

### Frontend

- React
- Vite
- npm

## Kubernetes

Kind cluster:

- 1 control-plane
- 3 workers
- NGINX Ingress Controller
- Metrics Server
- Helm
- HPA

## Deployment

Set the database URL:

    export DATABASE_URL="your-neon-database-url"

Create the Kind cluster:

    kind create cluster --name next-up --config k8s/kind/config.yml

Run the deployment script:

    ./deploy.sh

The script automatically:

- Builds frontend and backend Docker images
- Loads images into Kind
- Installs and configures NGINX Ingress
- Installs and configures Metrics Server
- Deploys the application with Helm

## Verify

    kubectl get pods -n next-up
    kubectl get services -n next-up
    kubectl get ingress -n next-up
    kubectl get hpa -n next-up

Test the application:

    curl http://localhost/
    curl http://localhost/api/health

## Load Testing

Run:

    k6 run k6/load-test.js

Watch HPA:

    kubectl get hpa -n next-up -w

Watch pods:

    kubectl get pods -n next-up -w