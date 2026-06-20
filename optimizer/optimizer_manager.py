import yaml
import requests
from logger import save_log
from optimizer.memory_optimizer import analyze_memory_and_cost
from optimizer.replica_cost_recommender import get_current_replicas
from rag.rag_engine import generate_alert_message
from optimizer.cpu_optimizer import analyze_cpu_and_cost
from logger import save_cpu_log

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

def main():
    # 1. تحميل الإعدادات
    with open("config.yaml", "r") as f:
        cfg = yaml.safe_load(f)
    
    opt_cfg = cfg.get('optimization', {})

    # 2. جلب البيانات من بروميثيوس
    actual_mem_bytes = get_prometheus_data('sum(container_memory_working_set_bytes{container="online-store"})')
    actual_mem_gb = actual_mem_bytes / (1024**3)
    
    current_replicas = get_current_replicas()


    actual_cpu = get_actual_cpu_usage()
    current_cpu_request = get_current_cpu_request()

    # 3. التحليل باستخدام قيم الـ config
    limit = opt_cfg.get('max_memory', 2.0)
    threshold = opt_cfg.get('replica_threshold', 0.3)
    min_replicas = opt_cfg.get('hpa_min_replicas', 2)
    
    recommended_mem, mem_cost = analyze_memory_and_cost(actual_mem_gb, limit)
    recommended_replicas = calculate_replica_recommendation(current_replicas, actual_mem_gb, limit, threshold, min_replicas)

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

    # 6. Build alert messages FIRST (fix critical bug)
    # 5. الحفظ
    
    cost_diff = mem_cost # تأكدي أن الدالة عندك تعيد القيمة الحقيقية
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
    Actual CPU Usage: {actual_cpu:.2f}m
    Recommended CPU: {recommended_cpu:.2f}m
    Current CPU Cost: ${current_cpu_cost:.2f}

    Optimized CPU Cost: ${optimized_cpu_cost:.2f}

    Expected Saving: ${cpu_saving:.2f}

    Estimated Savings: {cpu_saving_percent:.2f}%
    """


    # 4. الحفظ في الـ JSON (تأكدي من تمرير alert_text هنا)
    save_log("online-store", actual_mem_gb, recommended_mem, current_replicas, recommended_replicas, mem_cost, alert_text)


    save_cpu_log(
        "online-store",
        actual_cpu,
        current_cpu_request,
        recommended_cpu,
        cpu_saving,
        cpu_saving_percent,
        cpu_message
    )




    # 4. طباعة التقرير الموحد
    print(f"--- التقرير الموحد ---")
    print(f"الريبلكا الحالية : {int(current_replicas)}")
    print(f"الميموري الفعلي  : {actual_mem_gb:.2f} Gi")
    print(f"توصية الميموري    : {recommended_mem:.2f} Gi")
    print(f"توصية الريبلكا    : {recommended_replicas}")

    print(f"CPU Usage : {actual_cpu:.2f}m")
    print(f"CPU Request : {current_cpu_request:.2f}m")
    print(f"Recommended CPU : {recommended_cpu:.2f}m")
    print(f"CPU Saving : ${cpu_saving:.2f}")    

    print(f"----------------------")


    # 5. الطباعة الآن آمنة لأن alert_text تم تعريفه في الـ try/except
    print(f"\nتم توليد رسالة التنبيه:\n{alert_text}")


if __name__ == "__main__":
    main()
