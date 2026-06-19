# pricing_engine.py
# نستخدم الأسعار من مشروعك
PRICES = {
    "cpu_per_core_hour": 2.50,
    "mem_per_gb_hour": 0.65,
    "pod_unit_hour": 0.25
}

def calculate_optimized_cost(replicas,  mem_usage_gb):
    # معادلة الدمج بين الريبلكا والميموري
    cost_replicas = replicas * PRICES["pod_unit_hour"]
    cost_mem = mem_usage_gb * PRICES["mem_per_gb_hour"]
    return cost_replicas + cost_mem
