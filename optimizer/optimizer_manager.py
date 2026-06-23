import yaml
import requests
from logger import save_log
from optimizer.memory_optimizer import analyze_memory_and_cost
from optimizer.replica_cost_recommender import get_current_replicas
from rag.rag_engine import generate_alert_message
from optimizer.cpu_optimizer import analyze_cpu_and_cost
from optimizer.storage_optimizer import analyze_storage_and_cost

def get_prometheus_data(query):
    url = "http://localhost:9090/api/v1/query"
    try:
        response = requests.get(url, params={'query': query})
        data = response.json()
        if data.get('status') == 'success':
            results = data['data']['result']
            if results:
                total = sum([float(res['value'][1]) for res in results])
                return total
    except Exception as e:
        print(f"خطأ في الاتصال بـ Prometheus: {e}")
    return 0.0

def calculate_replica_recommendation(current_replicas, actual_mem_gb, limit, threshold, min_replicas):
    # نستخدم min_replicas من الـ config لضمان عدم النزول عن الحد المسموح
    if actual_mem_gb < (limit * threshold * current_replicas):
        return max(min_replicas, current_replicas - 1)
    return current_replicas

def get_actual_cpu_usage():
    query = '''
    sum(
        rate(
            container_cpu_usage_seconds_total{
                container="online-store"
            }[5m]
        )
    ) * 1000
    '''
    return get_prometheus_data(query)

import subprocess


def get_pod_metrics():
    try:
        output = subprocess.check_output(
            ["kubectl", "top", "pods", "--no-headers"]
        ).decode()

        total_cpu = 0
        total_mem = 0

        for line in output.splitlines():
            if "online-store" in line:
                parts = line.split()

                cpu = parts[1]
                mem = parts[2]

                total_cpu += int(cpu.replace("m", ""))
                total_mem += int(mem.replace("Mi", ""))

        return total_cpu, total_mem

    except Exception as e:
        print(f"Metrics error: {e}")
        return 0, 0

def get_current_cpu_request():
    query = '''
    sum(
        kube_pod_container_resource_requests{
            container="online-store",
            resource="cpu"
        }
    ) * 1000
    '''
    return get_prometheus_data(query)

def get_storage_metrics():
    capacity_query = '''
    sum(kubelet_volume_stats_capacity_bytes{
        persistentvolumeclaim="online-store"})'''
    used_query = '''
    sum(kubelet_volume_stats_used_bytes{
        persistentvolumeclaim="online-store"})'''

    capacity_bytes = get_prometheus_data(capacity_query)
    used_bytes = get_prometheus_data(used_query)
    capacity_gb = capacity_bytes / (1024**3)
    used_gb = used_bytes / (1024**3)

    return used_gb, capacity_gb

def calculate_total_cost_impact(memory_cost, cpu_cost, storage_cost):
    """
    Returns the total cost impact from memory and CPU optimizations.
    Positive value = savings.
    Negative value = additional cost.
    """
    return memory_cost + cpu_cost + storage_cost

def main():
    # 1. تحميل الإعدادات
    with open("config.yaml", "r") as f:
        cfg = yaml.safe_load(f)
    
    opt_cfg = cfg.get('optimization', {})

    # 2. جلب البيانات من بروميثيوس
    #actual_mem_bytes = get_prometheus_data('sum(container_memory_working_set_bytes{container="online-store"})')
    #actual_mem_gb = actual_mem_bytes / (1024**3)
    actual_cpu, actual_mem_mi = get_pod_metrics()
    actual_mem_gb = actual_mem_mi / 1024
    current_replicas = get_current_replicas()
    actual_storage_gb, allocated_storage_gb = get_storage_metrics()

    #actual_cpu = get_actual_cpu_usage()
    current_cpu_request = get_current_cpu_request()

    # 3. التحليل باستخدام قيم الـ config
    limit = opt_cfg.get('max_memory', 2.0)
    threshold = opt_cfg.get('replica_threshold', 0.3)
    min_replicas = opt_cfg.get('hpa_min_replicas', 2)
    
    (recommended_mem, mem_cost) = analyze_memory_and_cost(actual_mem_gb, limit)
    recommended_replicas = (calculate_replica_recommendation(current_replicas, actual_mem_gb, limit, threshold, min_replicas))

    (
        recommended_cpu,
        current_cpu_cost,
        optimized_cpu_cost,
        cpu_saving,
        cpu_saving_percent
    ) = analyze_cpu_and_cost(
        actual_cpu,
        current_cpu_request
    )
    (
    recommended_storage,
    current_storage_cost,
    optimized_storage_cost,
    storage_saving,
    storage_saving_percent
    ) = analyze_storage_and_cost(
    actual_storage_gb,
    allocated_storage_gb
    )

    total_cost_impact = (calculate_total_cost_impact(
        mem_cost,
        cpu_saving,
        storage_saving,
    ))

    # 6. Build alert messages FIRST (fix critical bug)
    # 5. الحفظ
    #cost_diff = mem_cost # تأكدي أن الدالة عندك تعيد القيمة الحقيقية
    current_stats = {"mem": f"{actual_mem_gb:.2f}Gi", "replicas": current_replicas}
    memory_stats = {
        "mem": f"{actual_mem_gb:.2f}Gi",
        "replicas": current_replicas
    }

    recommended_stats = {
        "mem": f"{recommended_mem:.2f}Gi",
        "replicas": recommended_replicas
    }

    try:
        alert_text = generate_alert_message(memory_stats, recommended_stats)
    except Exception as e:
        alert_text = f"Alert generation failed: {e}"


    cpu_message = f"""
    CPU Optimization Recommendation

    Current CPU Request: {current_cpu_request:.2f}m
   
    Recommended CPU: {recommended_cpu:.2f}m
    Current CPU Cost: ${current_cpu_cost:.2f}

    Optimized CPU Cost: ${optimized_cpu_cost:.2f}

    Expected Saving: ${cpu_saving:.2f}

    Estimated Savings: {cpu_saving_percent:.2f}%
    """

    storage_message = f"""
    Storage Optimization Recommendation

    Current Storage Allocation:{allocated_storage_gb:.2f} GB
    Current Storage Usage: {actual_storage_gb:.2f} GB
    Recommended Storage: {recommended_storage:.2f} GB
    Current Storage Cost:$ {current_storage_cost:.2f}
    Optimized Storage Cost:$ {optimized_storage_cost:.2f}
    Expected Saving: ${storage_saving:.2f}
    Estimated Savings: {storage_saving_percent:.2f}%
"""

    # 4. الحفظ في الـ JSON (تأكدي من تمرير alert_text هنا)
    #save_log("online-store", actual_mem_gb, recommended_mem, current_replicas, recommended_replicas, mem_cost, alert_text)




    # 4. طباعة التقرير الموحد
    print(f"--- التقرير الموحد ---")
    print(
        f"الريبلكا الحالية : "
        f"{int(current_replicas)}"
    )

    print(
        f"الميموري الفعلي : "
        f"{actual_mem_gb:.2f} Gi"
    )

    print(
        f"توصية الميموري : "
        f"{recommended_mem:.2f} Gi"
    )

    print(
        f"توصية الريبلكا : "
        f"{recommended_replicas}"
    )

    print(
        f"CPU Usage : "
        f"{actual_cpu:.2f}m"
    )

    print(
        f"CPU Request : "
        f"{current_cpu_request:.2f}m"
    )

    print(
        f"Recommended CPU : "
        f"{recommended_cpu:.2f}m"
    )

    print(
        f"CPU Saving : "
        f"${cpu_saving:.2f}"
    )

    print(
        f"Total Cost Impact : "
        f"${total_cost_impact:.2f}"
    )

    print(
        f"Storage Used : "
        f"{actual_storage_gb:.2f} GB"
    )
    print(
        f"Storage Allocated : "
        f"{allocated_storage_gb:.2f} GB"
    )
    print(
        f"Recommended Storage : "
        f"{recommended_storage:.2f} GB"
    )
    print(
        f"Storage Saving : "
        f"${storage_saving:.2f}"
    )

    print("----------------------")

    print(
        f"\nتم توليد رسالة التنبيه:\n"
        f"{alert_text}"
    )

    # Save ONE log entry
    save_log(
        service="online-store",
        actual_mem=actual_mem_gb,
        recommended_mem=recommended_mem,
        current_replicas=current_replicas,
        recommended_replicas=recommended_replicas,
        cost_diff=total_cost_impact,
        message={
            "memory_alert": alert_text,
            "cpu_alert": cpu_message,
            "storage_alert": storage_message,
        },
       # actual_cpu=actual_cpu,
        current_cpu_request=current_cpu_request,
        recommended_cpu=recommended_cpu,
        cpu_saving=cpu_saving,
       # cpu_saving_percent=cpu_saving_percent,
       current_storage=allocated_storage_gb,
       recommended_storage=recommended_storage,
       storage_saving=storage_saving
    )


if __name__ == "__main__":
    main()
