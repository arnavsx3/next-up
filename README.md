# NextUp

A simple queue management application where users can create and join queues using a unique room code.

Built as a hands-on Kubernetes, monitoring, autoscaling, and load-testing project.

## Architecture

```text
Cloudflare Tunnel
        ↓
NGINX Ingress
        ↓
React + Vite
        ↓
FastAPI
        ↓
Neon PostgreSQL
```

## Tech Stack

- **Frontend:** React, Vite
- **Backend:** Python, FastAPI, uv
- **Database:** Neon PostgreSQL
- **Web Server:** Nginx
- **Containerization:** Docker, Docker Compose
- **Orchestration:** Kubernetes, Kind, kubectl
- **Packaging:** Helm
- **Autoscaling:** HPA, VPA
- **Monitoring:** Prometheus, Grafana
- **Load Testing:** k6
- **External Access:** Cloudflare Tunnel

## Kubernetes

### 1. Create Cluster

```bash
kind create cluster --name next-up --config k8s/kind/config.yml
```

- 1 control-plane
- 3 workers
- Control-plane labeled `ingress-ready=true`
- Control-plane tainted `ingress-ready=true:NoSchedule`
- Host ports `80/443` → control-plane

### 2. Load Images

```bash
kind load docker-image next-up-backend:latest --name next-up
kind load docker-image next-up-frontend:latest --name next-up
```

### 3. Apply Application Resources

```bash
kubectl apply -f k8s/namespace.yml
kubectl apply -f k8s/configmaps.yml
kubectl apply -f k8s/secrets.yml

kubectl apply -f k8s/backend/
kubectl apply -f k8s/frontend/
```

### 4. Install NGINX Ingress

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

### 5. Patch Ingress Controller

Schedule it on the `ingress-ready` control-plane and allow it to tolerate the taint:

```bash
kubectl patch deployment ingress-nginx-controller -n ingress-nginx \
  --type='strategic' \
  -p '
spec:
  template:
    spec:
      nodeSelector:
        ingress-ready: "true"
      tolerations:
        - key: ingress-ready
          operator: Equal
          value: "true"
          effect: NoSchedule
'
```

### 6. Apply Ingress

```bash
kubectl apply -f k8s/ingress/ingress.yml
```

### 7. Verify

```bash
kubectl get nodes
kubectl get pods -n next-up
kubectl get services -n next-up
kubectl get pods -n ingress-nginx -o wide
kubectl get ingress -n next-up
```

### 8. Test

```bash
curl http://localhost/
curl http://localhost/api/health
```

## Kubernetes Flow

```text
localhost:80
     ↓
Kind Control Plane
     ↓
NGINX Ingress Controller
     ├── /      → frontend-service:80
     └── /api/* → backend-service:8000
```

## Rebuild After Code Changes

```bash
docker build -t next-up-backend:latest ./backend
kind load docker-image next-up-backend:latest --name next-up
kubectl rollout restart deployment next-up-backend-deployment -n next-up

docker build -t next-up-frontend:latest ./frontend
kind load docker-image next-up-frontend:latest --name next-up
kubectl rollout restart deployment next-up-frontend-deployment -n next-up
```