
import yaml
from pricing_engine import calculate_cpu_cost
def get_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)
def calculate_new_cpu_limit(actual_cpu_m):
    cfg = get_config()
    needed = actual_cpu_m * cfg['optimization']['cpu_safety_margin']
    return max(cfg['optimization']['min_cpu_millicores'], min(needed, cfg['optimization']['max_cpu_millicores']))
def analyze_cpu_and_cost(actual_cpu_m, current_cpu_request_m):
    recommended = calculate_new_cpu_limit(actual_cpu_m)
    current_cost = calculate_cpu_cost(current_cpu_request_m)
    optimized_cost = calculate_cpu_cost(recommended)
    saving = current_cost - optimized_cost
    if current_cost > 0:
        saving_percent = saving / current_cost * 100
    else:
        saving_percent = 0
    return (recommended, current_cost, optimized_cost, saving, saving_percent)