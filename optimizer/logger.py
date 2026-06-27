import json
from datetime import datetime


def save_log(
        service,

        current_memory,

        actual_mem,

        recommended_mem,

        memory_saving,



        current_replicas,

        actual_replicas,

        recommended_replicas,

        replica_saving,



        current_cpu_request,

        actual_cpu,

        recommended_cpu,

        cpu_saving,

        current_storage,

        actual_storage,

        recommended_storage,

        storage_saving,



        idle_nodes,

        unused_services,

        unused_apis,

        idle_saving,

        cost_diff,

        RAG_report,

    

):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "service_name": service,

        "memory": {
            "used":current_memory,
            "reserved": actual_mem,
            "recommended" :recommended_mem,
            "saved": memory_saving,
        },

        "replicas": {
           "used":current_replicas,
            "reserved": actual_replicas,
            "recommended" :recommended_replicas,
            "saved": replica_saving,
        },

        "cpu": {
          "used":current_cpu_request,
            "reserved": actual_cpu,
            "recommended" :recommended_cpu,
            "saved": cpu_saving,
        },


        "storage": {
           "used":current_storage,
            "reserved": actual_storage,
            "recommended" :recommended_storage,
            "saved": storage_saving,
        },

	"idle_resources": {
      	    "idle_nodes": idle_nodes,
   	    "unused_services": unused_services,
  	    "unused_apis": unused_apis,
       	    "saving": idle_saving
	},

        "cost_impact": cost_diff,
        "RAG_report": RAG_report
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
    return log_entry