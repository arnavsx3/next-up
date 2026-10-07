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

echo "==> Waiting for Ingress admission setup..."
kubectl wait \
  --for=condition=complete \
  job/ingress-nginx-admission-create \
  -n ingress-nginx \
  --timeout=180s

echo "==> Waiting for NGINX Ingress Controller..."
kubectl rollout status \
  deployment/ingress-nginx-controller \
  -n ingress-nginx \
  --timeout=180s

echo "==> Installing Metrics Server..."
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

echo "==> Patching Metrics Server for Kind..."
kubectl patch deployment metrics-server -n kube-system \
  --type='json' \
  -p='[
    {
      "op": "add",
      "path": "/spec/template/spec/containers/0/args/-",
      "value": "--kubelet-insecure-tls"
    }
  ]'

echo "==> Waiting for Metrics Server..."
kubectl rollout status \
  deployment/metrics-server \
  -n kube-system \
  --timeout=180s

# echo "==> Installing VPA..."
# git clone https://github.com/kubernetes/autoscaler.git
# cd autoscaler/vertical-pod-autoscaler
# ./hack/vpa-up.sh
# cd ../..
# rm -rf autoscaler

echo "==> Deploying Next-Up with Helm..."
helm upgrade --install next-up ./helm \
  --namespace next-up \
  --create-namespace \
  --set-string secret.databaseUrl="$DATABASE_URL"

echo "==> Deployment complete!"