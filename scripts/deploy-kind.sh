#!/bin/bash

set -e

CLUSTER_NAME="next-up"

echo "==> Building images..."
docker build -t next-up-backend:latest ./backend
docker build -t next-up-frontend:latest ./frontend

echo "==> Loading images into Kind..."
kind load docker-image next-up-backend:latest --name "$CLUSTER_NAME"
kind load docker-image next-up-frontend:latest --name "$CLUSTER_NAME"

echo "==> Installing NGINX Ingress Controller..."
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

echo "==> Patching Ingress Controller..."
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

echo "==> Deploying Next-Up with Helm..."
helm upgrade --install next-up ./helm \
  --namespace next-up \
  --create-namespace \
  --set-string secret.databaseUrl="$DATABASE_URL"

echo "==> Deployment complete!"