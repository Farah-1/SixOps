# Prometheus Queries - Online Store HPA Pack

## Current Deployment Replicas
kube_deployment_status_replicas{deployment="online-store", namespace="default"}

## Available Replicas
kube_deployment_status_replicas_available{deployment="online-store", namespace="default"}

## HPA Current Replicas
kube_horizontalpodautoscaler_status_current_replicas{horizontalpodautoscaler="online-store-hpa", namespace="default"}

## HPA Desired Replicas
kube_horizontalpodautoscaler_status_desired_replicas{horizontalpodautoscaler="online-store-hpa", namespace="default"}

## HPA Max Replicas
kube_horizontalpodautoscaler_spec_max_replicas{horizontalpodautoscaler="online-store-hpa", namespace="default"}

## HPA Min Replicas
kube_horizontalpodautoscaler_spec_min_replicas{horizontalpodautoscaler="online-store-hpa", namespace="default"}

## CPU Usage Per Pod
sum(rate(container_cpu_usage_seconds_total{namespace="default", pod=~"online-store.*", container!="", image!=""}[5m])) by (pod)

## Memory Usage Per Pod
container_memory_usage_bytes{namespace="default", pod=~"online-store.*", container!="", image!=""}

## Pod Restarts
kube_pod_container_status_restarts_total{namespace="default", pod=~"online-store.*"}
