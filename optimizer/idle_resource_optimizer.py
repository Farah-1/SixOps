
import yaml
import subprocess
def get_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)
def run_command(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return result.strip()
    except Exception:
        return ''
def count_idle_nodes():
    output = run_command('kubectl top nodes --no-headers')
    if output == '':
        return 0
    else:
        cfg = get_config()
        cpu_threshold = cfg['optimization']['idle_node_cpu_threshold']
        mem_threshold = cfg['optimization']['idle_node_memory_threshold']
        idle_nodes = 0
        for line in output.splitlines():
            parts = line.split()
            if len(parts) < 5:
                continue
            else:
                cpu_percent = int(parts[2].replace('%', ''))
                mem_percent = int(parts[4].replace('%', ''))
                if cpu_percent < cpu_threshold and mem_percent < mem_threshold:
                        idle_nodes += 1
        return idle_nodes
def count_unused_services():
    output = run_command('kubectl get endpoints --all-namespaces')
    if output == '':
        return 0
    else:
        unused = 0
        for line in output.splitlines()[1:]:
            if '<none>' in line:
                unused += 1
        return unused
def count_unused_apis():
    """\n    Demo implementation.\n\n    Assume:\n    app.py has 10 APIs.\n    Metrics show only 6 called.\n\n    Therefore:\n    4 APIs are unused.\n    """
    total_apis = 10
    used_apis = 6
    return total_apis - used_apis
def analyze_idle_resources():
    cfg = get_config()
    idle_nodes = count_idle_nodes()
    unused_services = count_unused_services()
    unused_apis = count_unused_apis()
    node_cost = idle_nodes * cfg['optimization']['idle_node_cost_per_hour']
    service_cost = unused_services * cfg['optimization']['unused_service_cost']
    api_cost = unused_apis * cfg['optimization']['unused_api_cost']
    total_saving = node_cost + service_cost + api_cost
    return (idle_nodes, unused_services, unused_apis, total_saving)