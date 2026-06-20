import json
from datetime import datetime

def save_log(service, actual_mem, recommended_mem, current_replicas, recommended_replicas, cost_diff, message):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "service_name": service,
        "memory": {"actual": actual_mem, "recommended": recommended_mem},
        "replicas": {"current": current_replicas, "recommended": recommended_replicas},
        "cost_impact": cost_diff,
        "alert_message": message
    }
    with open("optimization_log.json", "a", encoding="utf-8") as f:
        # إضافة indent=4 تجعل الـ JSON يظهر بتنسيق "شجري" جميل
        f.write(json.dumps(log_entry, ensure_ascii=False, indent=4) + "\n")
    

def save_cpu_log(
        service,
        actual_cpu,
        current_cpu_request,
        recommended_cpu,
        saving,
        saving_percent,
        message):

    log_entry = {
    	"timestamp": datetime.now().isoformat(),
    	"service_name": service,
    	"cpu": {
        	"actual_usage_millicores": actual_cpu,
        	"current_request_millicores": current_cpu_request,
        	"recommended_request_millicores": recommended_cpu
    	},
    	"cpu_cost_saving": saving,
    	"cpu_saving_percentage": saving_percent,
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
