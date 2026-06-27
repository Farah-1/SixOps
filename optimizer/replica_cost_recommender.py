
import subprocess
import math
from pricing_engine import calculate_optimized_cost
DEPLOYMENT_NAME = 'online-store'
NAMESPACE = 'default'
COST_PER_REPLICA_PER_HOUR = 0.1
CPU_REQUEST_MILLICORES = 100
TARGET_CPU_PERCENT = 60
TARGET_CPU_MILLICORES = CPU_REQUEST_MILLICORES * TARGET_CPU_PERCENT / 100
def run_command(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return result.strip()
    except subprocess.CalledProcessError:
        return ''
def get_current_replicas():
    command = (
        f"kubectl get deployment {DEPLOYMENT_NAME} "
        f"-n {NAMESPACE} "
        f"-o jsonpath='{{.status.replicas}}'"
    )
    output = run_command(command)
    if output == '':
        return 0
    else:
        return int(output)



def parse_cpu_to_millicores(cpu_value):
    """\n    Examples:\n    5m  -> 5\n    100m -> 100\n    1   -> 1000\n    """
    cpu_value = cpu_value.strip()
    if cpu_value.endswith('m'):
        return int(cpu_value.replace('m', ''))
    else:
        return int(float(cpu_value) * 1000)
def get_total_cpu_usage_millicores():
    command = f'kubectl top pods -n {NAMESPACE} -l app={DEPLOYMENT_NAME} --no-headers'
    output = run_command(command)
    if output == '':
        return
    else:
        total_cpu = 0
        pod_count = 0
        for line in output.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                cpu_value = parts[1]
                total_cpu += parse_cpu_to_millicores(cpu_value)
                pod_count += 1
        if pod_count == 0:
            return
        else:
            return total_cpu
def recommend_needed_replicas(current_replicas, total_cpu_millicores):
    """\n    Formula:\n    needed replicas = total CPU usage / target CPU per pod\n\n    Example:\n    total CPU = 120m\n    target per pod = 60m\n    needed replicas = 2\n    """
    if total_cpu_millicores is None:
        return 2
    else:
        needed = math.ceil(total_cpu_millicores / TARGET_CPU_MILLICORES)
        needed = max(2, needed)
        needed = min(needed, current_replicas)
        return needed
def analyze_replica_and_cost(current_replicas, total_cpu_millicores):
    recommended_replicas = recommend_needed_replicas(current_replicas, total_cpu_millicores)
    current_cost = calculate_optimized_cost(current_replicas, current_replicas * 0.5)
    optimized_cost = calculate_optimized_cost(recommended_replicas, recommended_replicas * 0.5)
    saving = current_cost - optimized_cost
    if current_cost > 0:
        saving_percent = saving / current_cost * 100
    else:
        saving_percent = 0
    return (recommended_replicas, current_cost, optimized_cost, saving, saving_percent)
def get_actual_running_replicas():
    try:
        output = subprocess.check_output(['kubectl', 'get', 'deployment', 'online-store', '-o', 'jsonpath={.status.readyReplicas}'], text=True).strip()
        return int(output) if output else 0
    except:
        return 0
def main():
    current_replicas = get_current_replicas()
    if current_replicas == 0:
        return
    else:
        total_cpu = get_total_cpu_usage_millicores()
        needed_replicas = recommend_needed_replicas(current_replicas, total_cpu)
        needed_replicas, current_cost, optimized_cost, saving, saving_percent = analyze_replica_and_cost(current_replicas, total_cpu)
if __name__ == '__main__':
    main()