# NextUp

A simple queue management app built as a hands-on project for Kubernetes, Helm, autoscaling, monitoring, and load testing.

## Autoscaling Demo

A k6 load test pushes CPU up on the backend, the HPA reacts, and Grafana shows the pods scaling in real time.

![Grafana dashboard showing HPA scaling the backend](docs/grafana-hpa.jpg)

- **Top left:** the backend scaled from 1 to 5 pods (dashed line = what the HPA wanted).
- **Top right and bottom:** CPU per pod rises above the HPA target, then drops as the load spreads across new pods.
- The frontend stayed at 1 pod because it uses almost no CPU.

## Architecture

```mermaid
flowchart LR
    User --> Ingress[NGINX Ingress]
    Ingress --> FE[Frontend: React + Vite]
    Ingress --> BE[Backend: FastAPI]
    BE --> DB[(Neon PostgreSQL)]
    HPA -. scales .-> BE
    HPA -. scales .-> FE
    Prom[Prometheus + Grafana] -. watches .-> BE
    K6[k6] -- load --> Ingress
```

## Tech Stack

| Area | Tools |
|---|---|
| Frontend | React, Vite |
| Backend | Python, FastAPI, uv, SQLAlchemy, python-dotenv |
| Database | Neon PostgreSQL |
| Containers | Docker, Docker Compose |
| Kubernetes | Kind, kubectl, Helm |
| Ingress | NGINX Ingress Controller |
| Autoscaling | HPA, Kubernetes Metrics Server |
| Monitoring | Prometheus, Grafana (kube-prometheus-stack) |
| Load testing | k6 |

## Project Structure

```
backend/        FastAPI app and Dockerfile
frontend/       React app and Dockerfile
helm/           Helm chart (deployments, services, ingress, HPA)
k8s/kind/       Kind cluster config
k6/             Load test
monitoring/     Prometheus/Grafana values and dashboard JSON
scripts/        Deployment scripts
docs/           Screenshots
```

## Prerequisites

- Docker
- Kind
- kubectl
- Helm
- Python and uv
- Node.js and npm
- k6

## Getting Started

### 1. Set the database URL

Create `backend/.env`:

```
DATABASE_URL=postgresql+psycopg://user:password@host/dbname?sslmode=require
```

Do not put quotes around the value. `backend/.env` is ignored by Git, so your credentials stay local.

### 2. Create the Kind cluster

```bash
kind create cluster --name next-up --config k8s/kind/config.yml
```

The cluster has 1 control-plane node and 3 workers.

### 3. Deploy

```bash
./scripts/deploy-kind.sh
```

The script:

- Builds the frontend and backend Docker images
- Loads the images into Kind
- Installs and configures NGINX Ingress
- Installs and configures Metrics Server
- Creates the `next-up-secrets` Kubernetes Secret from `backend/.env`
- Deploys the app with Helm

### 4. Verify

```bash
kubectl get pods -n next-up
kubectl get services -n next-up
kubectl get ingress -n next-up
kubectl get hpa -n next-up
```

```bash
curl http://localhost/
curl http://localhost/api/health
```

## Monitoring

Install Prometheus and Grafana:

```bash
./scripts/deploy-monitoring.sh
```

Open Grafana:

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
```

Then go to http://localhost:3000, open **Dashboards → New → Import**, and upload `monitoring/next-up-hpa-dashboard.json`.

The dashboard shows pods per deployment, the HPA desired replicas, CPU per pod, and CPU as a percentage of the request (the value the HPA watches).

## Load Testing

Run the test:

```bash
k6 run k6/load-test.js
```

In other terminals, watch the HPA and pods:

```bash
kubectl get hpa -n next-up -w
kubectl get pods -n next-up -w
```

The test ramps up to 50 virtual users over about 2.5 minutes and checks that both the frontend and `/api/health` return 200.

## Notes

- **Autoscaling at startup:** a pod uses extra CPU while it starts. With a small CPU request this can look like high load and trigger a scale-up. Tune `resources.requests.cpu` and the HPA target in `helm/values.yaml`.
- **Scale down is slow on purpose:** the HPA waits about 5 minutes before removing pods.
- **Secrets:** the app reads `DATABASE_URL` from a Kubernetes Secret created by the deploy script. A secrets manager such as Infisical is a good next step.