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