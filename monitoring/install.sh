#!/bin/bash

set -e

NAMESPACE="monitoring"
RELEASE_NAME="monitoring"

echo "==> Adding Prometheus Community Helm repository..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

echo "==> Creating monitoring namespace..."
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

echo "==> Installing Prometheus + Grafana..."
helm upgrade --install "$RELEASE_NAME" \
  prometheus-community/kube-prometheus-stack \
  --namespace "$NAMESPACE" \
  --values ./monitoring/values.yaml

echo "==> Waiting for monitoring stack..."
kubectl rollout status deployment/"$RELEASE_NAME"-grafana \
  -n "$NAMESPACE" \
  --timeout=180s

echo "==> Monitoring stack deployed!"