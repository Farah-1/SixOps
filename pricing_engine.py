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

def calculate_cpu_cost(cpu_millicores):
    cpu_cores = cpu_millicores / 1000
    return cpu_cores * PRICES["cpu_per_core_hour"]

def calculate_storage_cost(storage_gb):
    STORAGE_PRICE_PER_GB = 0.10
    return storage_gb * STORAGE_PRICE_PER_GB