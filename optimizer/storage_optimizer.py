import yaml
from pricing_engine import calculate_storage_cost


def get_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


def calculate_new_storage_limit(actual_storage_gb):
    cfg = get_config()

    needed = (
        actual_storage_gb *
        cfg['optimization']['storage_safety_margin']
    )

    return max(
        cfg['optimization']['min_storage_gb'],
        min(
            needed,
            cfg['optimization']['max_storage_gb']
        )
    )


def analyze_storage_and_cost(
        actual_storage_gb,
        current_storage_gb):

    recommended = calculate_new_storage_limit(
        actual_storage_gb
    )

    current_cost = calculate_storage_cost(
        current_storage_gb
    )

    optimized_cost = calculate_storage_cost(
        recommended
    )

    saving = current_cost - optimized_cost

    if current_cost > 0:
        saving_percent = (
            saving / current_cost
        ) * 100
    else:
        saving_percent = 0

    return (
        recommended,
        current_cost,
        optimized_cost,
        saving,
        saving_percent
    )
