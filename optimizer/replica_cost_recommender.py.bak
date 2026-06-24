import subprocess
import math
from pricing_engine import calculate_optimized_cost

DEPLOYMENT_NAME = "online-store"
NAMESPACE = "default"

# Cost assumption for demo
COST_PER_REPLICA_PER_HOUR = 0.10

# Kubernetes resource request from deployment.yaml
CPU_REQUEST_MILLICORES = 100

# HPA target CPU utilization
TARGET_CPU_PERCENT = 60
TARGET_CPU_MILLICORES = CPU_REQUEST_MILLICORES * TARGET_CPU_PERCENT / 100


def run_command(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return result.strip()
    except subprocess.CalledProcessError:
        return ""


def get_current_replicas():
    command = (
        f"kubectl get deployment {DEPLOYMENT_NAME} "
        f"-n {NAMESPACE} "
        f"-o jsonpath='{{.status.replicas}}'"
    )
    output = run_command(command)

    if output == "":
        return 0

    return int(output)


def parse_cpu_to_millicores(cpu_value):
    """
    Examples:
    5m  -> 5
    100m -> 100
    1   -> 1000
    """
    cpu_value = cpu_value.strip()

    if cpu_value.endswith("m"):
        return int(cpu_value.replace("m", ""))

    return int(float(cpu_value) * 1000)


def get_total_cpu_usage_millicores():
    command = f"kubectl top pods -n {NAMESPACE} -l app={DEPLOYMENT_NAME} --no-headers"
    output = run_command(command)

    if output == "":
        return None

    total_cpu = 0
    pod_count = 0

    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            cpu_value = parts[1]
            total_cpu += parse_cpu_to_millicores(cpu_value)
            pod_count += 1

    if pod_count == 0:
        return None

    return total_cpu


def recommend_needed_replicas(current_replicas, total_cpu_millicores):
    """
    Formula:
    needed replicas = total CPU usage / target CPU per pod

    Example:
    total CPU = 120m
    target per pod = 60m
    needed replicas = 2
    """
    if total_cpu_millicores is None:
        # Fallback for demo if metrics-server is not available
        return 2

    needed = math.ceil(total_cpu_millicores / TARGET_CPU_MILLICORES)

    # Keep at least 2 replicas for availability
    needed = max(2, needed)

    # Do not recommend more than current replicas in cost optimization mode
    needed = min(needed, current_replicas)

    return needed


def calculate_cost(current_replicas, needed_replicas):
    # هنا سنفترض ميموري ثابتة للريبلكا (مثلاً 0.5 جيجا) لحين دمج الميموري
    current_cost = calculate_optimized_cost(current_replicas, current_replicas * 0.5)
    optimized_cost = calculate_optimized_cost(needed_replicas, needed_replicas * 0.5)
    saving = current_cost - optimized_cost

    # حفظ الـ Log باستخدام ملفك الجديد
    from logger import save_log
    save_log("online-store", current_replicas, needed_replicas, saving)

    return current_cost, optimized_cost, saving


def main():
    current_replicas = get_current_replicas()

    if current_replicas == 0:
        print("Deployment not found or replicas are zero.")
        return

    total_cpu = get_total_cpu_usage_millicores()
    needed_replicas = recommend_needed_replicas(current_replicas, total_cpu)

    current_cost, optimized_cost, saving, saving_percent = calculate_cost(
        current_replicas,
        needed_replicas
    )

    print("=" * 60)
    print("Replica / HPA Optimization Report")
    print("=" * 60)

    print(f"Application: {DEPLOYMENT_NAME}")
    print(f"Current replicas: {current_replicas}")

    if total_cpu is None:
        print("Total CPU usage: Not available")
        print("Note: metrics-server may not be ready. Using fallback needed replicas = 2")
    else:
        print(f"Total CPU usage: {total_cpu}m")
        print(f"Target CPU per pod: {TARGET_CPU_MILLICORES}m")

    print(f"Actual needed replicas: {needed_replicas}")
    print(f"Current cost per hour: ${current_cost:.2f}")
    print(f"Optimized cost per hour: ${optimized_cost:.2f}")
    print(f"Expected saving per hour: ${saving:.2f}")
    print(f"Expected saving percentage: {saving_percent:.2f}%")

    print()
    print("Recommendation:")
    print(f"Enable HPA with minReplicas={needed_replicas}, maxReplicas={current_replicas}, targetCPU={TARGET_CPU_PERCENT}%")

    print()
    print("Suggested HPA command:")
    print(
        f"kubectl autoscale deployment {DEPLOYMENT_NAME} "
        f"--cpu-percent={TARGET_CPU_PERCENT} "
        f"--min={needed_replicas} "
        f"--max={current_replicas}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
