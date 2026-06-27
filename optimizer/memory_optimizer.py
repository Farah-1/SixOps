
import yaml
from pricing_engine import calculate_optimized_cost
def get_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)
def calculate_new_memory_limit(actual_usage_gb):
    cfg = get_config()
    needed = actual_usage_gb * cfg['optimization']['safety_margin']
    return max(cfg['optimization']['min_memory'], min(needed, cfg['optimization']['max_memory']))
def analyze_memory_and_cost(actual_usage_gb, current_limit_gb):
    recommended = calculate_new_memory_limit(actual_usage_gb)
    current_cost = calculate_optimized_cost(1, current_limit_gb)
    optimized_cost = calculate_optimized_cost(1, recommended)
    saving = current_cost - optimized_cost
    if current_cost > 0:
        saving_percent = saving / current_cost * 100
    else:
        saving_percent = 0
    return (recommended, current_cost, optimized_cost, saving, saving_percent)
# def get_current_memory_request_from_k8s():
#     try:
#         output = subprocess.check_output(['kubectl', 'get', 'deployment', 'online-store', '-o', 'jsonpath={.spec.template.spec.containers[0].resources.requests.memory}'], text=True).strip()
#         if output.endswith('Mi'):
#             return float(output[:(-2)]) / 1024
#         else:
#             return float(output)
#     except Exception:
#         return 0.0
import json
import subprocess
def get_current_memory_request_from_k8s():
    # ***<module>.get_current_memory_request_from_k8s: Failure: Different control flow
    try:
        cmd = ['kubectl', 'get', 'deployment', 'online-store', '-o', 'json']
        output = subprocess.check_output(cmd, text=True)
        data = json.loads(output)
        containers = data['spec']['template']['spec']['containers']
        for container in containers:
            if container['name'] == 'online-store':
                mem = container.get('resources', {}).get('requests', {}).get('memory', '0Mi')
                if 'm' in mem and 'Mi' not in mem:
                    return float(mem.replace('m', '')) / 1024
                else:
                    if 'Mi' in mem:
                        return float(mem.replace('Mi', '')) / 1024
                    else:
                        if 'Gi' in mem:
                            return float(mem.replace('Gi', ''))
    except Exception as e:
        return 0.0 + (None, e, e)
    return 0.0