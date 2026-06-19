import yaml
from pricing_engine import calculate_optimized_cost

def get_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def calculate_new_memory_limit(actual_usage_gb):
    cfg = get_config()
    # المعادلة: الاستخدام الفعلي × معامل الأمان (مع الالتزام بالـ Min/Max)
    needed = actual_usage_gb * cfg['optimization']['safety_margin']
    return max(cfg['optimization']['min_memory'], min(needed, cfg['optimization']['max_memory']))

def analyze_memory_and_cost(actual_usage_gb, current_limit_gb):
    recommended = calculate_new_memory_limit(actual_usage_gb)
    cost = calculate_optimized_cost(1, recommended) # افتراض 1 ريبلكا للتبسيط
    return recommended, cost
