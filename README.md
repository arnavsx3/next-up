# NextUp

A simple queue management application where users can create and join queues using a unique room code.  
Built primarily as a hands-on Kubernetes, monitoring, autoscaling, and load-testing project.

## Architecture

Cloudflare Tunnel  
↓  
Nginx Ingress  
↓  
React + Vite (Frontend)  
↓  
FastAPI (Backend)  
↓  
Neon PostgreSQL

The application runs on a multi-node **Kind Kubernetes cluster**.

Kubernetes:
- Deployments
- Services
- Ingress
- ConfigMaps
- Secrets
- HPA
- VPA
- Metrics Server
- Resource Requests & Limits
- Liveness & Readiness Probes

Monitoring:
- Prometheus
- Grafana

Load Testing:
- k6

Containerization:
- Docker
- Docker Compose

Kubernetes Packaging:
- Helm

External Access:
- Cloudflare Tunnel

## Tech Stack

- **Frontend:** React, Vite
- **Backend:** Python, FastAPI, uv
- **Database:** Neon PostgreSQL
- **Web Server:** Nginx
- **Containerization:** Docker, Docker Compose
- **Orchestration:** Kubernetes, Kind, kubectl
- **Kubernetes Packaging:** Helm
- **Autoscaling:** HPA, VPA
- **Monitoring:** Prometheus, Grafana
- **Load Testing:** k6
- **External Access:** Cloudflare Tunnel

## K8s

# 1. Create the Kind cluster
kind create cluster --name next-up --config k8s/kind/config.yml

# 2. Load your locally-built images into the Kind nodes
kind load docker-image next-up-backend:latest --name next-up
kind load docker-image next-up-frontend:latest --name next-up

# 3. Create namespace + config/secrets
kubectl apply -f k8s/namespace.yml
kubectl apply -f k8s/configmap.yml
kubectl apply -f k8s/secret.yml

# 4. Deploy backend + frontend
kubectl apply -f k8s/backend/
kubectl apply -f k8s/frontend/

# 5. Install NGINX Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# 6. Wait for Ingress Controller
kubectl get pods -n ingress-nginx -w
# Ctrl+C once the controller is 1/1 Running

# 7. Apply your Ingress
kubectl apply -f k8s/ingress/ingress.yml

# 8. Verify everything
kubectl get pods -n next-up
kubectl get services -n next-up
kubectl get ingress -n next-up