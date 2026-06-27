import yaml

import sys

import os

import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



import requests

from logger import save_log

from optimizer.memory_optimizer import *

#from optimizer.replica_cost_recommender import get_current_replicas

from optimizer.replica_cost_recommender import *

from optimizer.storage_optimizer import analyze_storage_and_cost

from rag.rag_engine import generate_alert_message

from optimizer.cpu_optimizer import analyze_cpu_and_cost

from optimizer.idle_resource_optimizer import (

    analyze_idle_resources

)





def get_prometheus_data(query):

    url = "http://localhost:46691/api/v1/query"

    try:

        response = requests.get(url, params={'query': query})

        data = response.json()

        if data.get('status') == 'success':

            results = data['data']['result']

            if results:

                total = sum([float(res['value'][1]) for res in results])

                return total

    except Exception as e:
            {}

    return 0.0



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

    sum(

        kubelet_volume_stats_capacity_bytes{

            persistentvolumeclaim="online-store"

        }

    )

    '''



    used_query = '''

    sum(

        kubelet_volume_stats_used_bytes{

            persistentvolumeclaim="online-store"

        }

    )

    '''



    capacity_bytes = get_prometheus_data(

        capacity_query

    )



    used_bytes = get_prometheus_data(

        used_query

    )



    capacity_gb = capacity_bytes / (1024 ** 3)

    used_gb = used_bytes / (1024 ** 3)



    return (

        used_gb,

        capacity_gb

    )





def calculate_total_cost_impact(memory_cost, cpu_cost, replica_saving, storage_saving, idle_saving):

    """

    Returns the total cost impact from memory and CPU optimizations.

    Positive value = savings.

    Negative value = additional cost.

    """

    return memory_cost + cpu_cost + replica_saving + storage_saving + idle_saving



def get_current_cpu_request_from_k8s():

    try:

        output = subprocess.check_output(

            [

                "kubectl",

                "get",

                "deployment",

                "online-store",

                "-o",

                "jsonpath={.spec.template.spec.containers[0].resources.requests.cpu}",

            ],

            text=True,

        ).strip()



        if output.endswith("m"):

            return float(output[:-1])



        return float(output) * 1000



    except Exception:

        return 0.0





def main():

    # 1. تحميل الإعدادات

    with open("config.yaml", "r") as f:

        cfg = yaml.safe_load(f)

    

    opt_cfg = cfg.get('optimization', {})



    

    actual_cpu, actual_mem_mi = get_pod_metrics()

    actual_mem_gb = actual_mem_mi / 1024

    current_replicas = get_current_replicas()
    reserved_mem_gb = get_current_memory_request_from_k8s()

    actual_running_replicas = get_actual_running_replicas()



    actual_storage_gb, current_storage_gb = (

        get_storage_metrics()

    )



  

    current_cpu_request = get_current_cpu_request()



    if current_cpu_request == 0:

        current_cpu_request = get_current_cpu_request_from_k8s()






    (

        recommended_mem,

        current_memory_cost,

        optimized_memory_cost,

        memory_saving,

        memory_saving_percent

    ) = analyze_memory_and_cost(

        actual_mem_gb,

        reserved_mem_gb

    )





    (

        recommended_replicas,

        current_replica_cost,

        optimized_replica_cost,

        replica_saving,

        replica_saving_percent

    ) = analyze_replica_and_cost(

        current_replicas,

        actual_cpu

    )



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

        current_storage_gb

    )





    (

        idle_nodes,

        unused_services,

        unused_apis,

        idle_saving

    ) = analyze_idle_resources()









    total_cost_impact = (calculate_total_cost_impact(

memory_saving,

        cpu_saving,

replica_saving,

storage_saving,

idle_saving

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



# تجميع البيانات في قاموس واحد شامل
    report_data = {
        "service": "online-store",
        "current_memory": reserved_mem_gb,
        "recommended_mem": recommended_mem,
        "current_cpu": current_cpu_request,
        "recommended_cpu": recommended_cpu,
        "current_replicas": current_replicas,
        "recommended_replicas": recommended_replicas,
        "current_storage": current_storage_gb,
        "recommended_storage": recommended_storage,
        "total_saving": total_cost_impact
    }

    # استدعاء الفانكشن وتمرير القاموس لها
    try:
        alert_text = generate_alert_message(report_data)
    except Exception as e:
        alert_text = f"Alert generation failed: {e}"



    data= save_log(

        service="online-store",

        current_memory=reserved_mem_gb,

        actual_mem=actual_mem_gb,

        recommended_mem=recommended_mem,

        memory_saving=memory_saving,



        current_replicas=current_replicas,

        actual_replicas=actual_running_replicas,

        recommended_replicas=recommended_replicas,

        replica_saving=replica_saving,



        current_cpu_request=current_cpu_request,

        actual_cpu=actual_cpu,

        recommended_cpu=recommended_cpu,

        cpu_saving=cpu_saving,

        

        

        current_storage=current_storage_gb,

        actual_storage=actual_storage_gb,

        recommended_storage=recommended_storage,

        storage_saving=storage_saving,



        idle_nodes=idle_nodes,

        unused_services=unused_services,

        unused_apis=unused_apis,

        idle_saving=idle_saving,

        cost_diff=total_cost_impact,

        RAG_report= alert_text,

    

    )
    print(json.dumps(data))









if __name__ == "__main__":

    main() 

