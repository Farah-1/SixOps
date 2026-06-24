import json
from datetime import datetime

#def save_log(service, actual_mem, recommended_mem, current_replicas, recommended_replicas, cost_diff, message, current_cpu_request, recommended_cpu, cpu_saving):
#    log_entry = {
#        "timestamp": datetime.now().isoformat(),
#        "service_name": service,
#        "memory": {"actual": actual_mem, "recommended": recommended_mem},
#        "replicas": {"current": current_replicas, "recommended": recommended_replicas},
#        "cpu":{"current": current_cpu_request, "recommended": recommended_cpu },
#        "cost_impact": cost_diff,
#        "alert_message": message
#    }
#    with open("optimization_log.json", "a", encoding="utf-8") as f:
#        # إضافة indent=4 تجعل الـ JSON يظهر بتنسيق "شجري" جميل
#        f.write(json.dumps(log_entry, ensure_ascii=False, indent=4) + "\n")


def save_log(
        service,
        actual_mem,
        recommended_mem,
        current_replicas,
        recommended_replicas,
        cost_diff,
        message,
        current_cpu_request,
        recommended_cpu,
        cpu_saving,
        current_replica_cost=0,
        optimized_replica_cost=0,
        replica_saving=0,
        replica_saving_percent=0,
        current_storage=0,
        recommended_storage=0,
        storage_saving=0
):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "service_name": service,

        "memory": {
            "actual": actual_mem,
            "recommended": recommended_mem
        },

        "replicas": {
            "current": current_replicas,
            "recommended": recommended_replicas,
            "current_cost": current_replica_cost,
            "optimized_cost": optimized_replica_cost,
            "saving": replica_saving,
            "saving_percent": replica_saving_percent
        },

        "cpu": {
            "current": current_cpu_request,
            "recommended": recommended_cpu,
            "saving": cpu_saving
        },


        "storage": {
            "current": current_storage,
            "recommended": recommended_storage,
            "saving": storage_saving
        },

        "cost_impact": cost_diff,
        "alert_message": message
    }

    with open(
        "optimization_log.json",
        "a",
        encoding="utf-8"
    ) as f:
        f.write(
            json.dumps(
                log_entry,
                ensure_ascii=False,
                indent=4
            ) + "\n"
        )
