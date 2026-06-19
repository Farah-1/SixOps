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
    

