# Replica / HPA Optimization Explanation

The Online Store application was initially deployed with 6 replicas.

Running too many replicas without enough traffic increases infrastructure cost because each replica consumes CPU and memory resources.

The optimizer checks the current replica count and CPU usage. Then it estimates the actual needed replicas based on the HPA CPU target.

The cost calculation is:

Current cost = current replicas × cost per replica per hour

Optimized cost = needed replicas × cost per replica per hour

Expected saving = current cost - optimized cost

If the application is over-provisioned, the system recommends enabling Horizontal Pod Autoscaler.

For this demo:
- Current replicas: 6
- Actual needed replicas: 2
- Recommended HPA minReplicas: 2
- Recommended HPA maxReplicas: 6
- Target CPU utilization: 60%

HPA allows Kubernetes to scale the application up during high traffic and scale it down during low traffic.

This improves performance during load spikes and reduces unnecessary cost when traffic is low.
