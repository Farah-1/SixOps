import json
import sys
import joblib
import pandas as pd


MODEL_FILE = "cost-anomaly-alerting-pack/ai/models/random_forest_anomaly_model.pkl"
DEFAULT_INPUT_FILE = "cost-anomaly-alerting-pack/ai/processed/clean_cloud_dataset.csv"
DEFAULT_OUTPUT_FILE = "cost-anomaly-alerting-pack/ai/output/ai_predictions.json"
features = [
    "CPU_Usage",
    "Memory_Usage",
    "Disk_IO",
    "Network_IO",
    "Workload_Type",
    "hour",
    "day",
    "day_of_week",
]


def prepare_input(df):
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df["hour"] = df["Timestamp"].dt.hour
        df["day"] = df["Timestamp"].dt.day
        df["day_of_week"] = df["Timestamp"].dt.dayofweek

    if "User_ID" in df.columns:
        df = df.drop(columns=["User_ID"])

    for column in ["CPU_Usage", "Memory_Usage", "Disk_IO", "Network_IO"]:
        df[column] = df[column].clip(lower=0)

    return df


input_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT_FILE
output_file = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT_FILE

model = joblib.load(MODEL_FILE)
df = pd.read_csv(input_file)
df = prepare_input(df)

sample = df[features]

predictions = model.predict(sample)
probabilities = model.predict_proba(sample)[:, 1]

def build_explanation(is_anomaly, row):
    if not is_anomaly:
        return "Resource utilization is within the expected operating range."

    reasons = []

    if row["CPU_Usage"] >= 80:
        reasons.append("high CPU usage")

    if row["Memory_Usage"] >= 75:
        reasons.append("high memory usage")

    if row["Disk_IO"] >= 40:
        reasons.append("high disk I/O")

    if row["Network_IO"] >= 30:
        reasons.append("high network I/O")

    if row["Workload_Type"] == "Crypto_Mining":
        reasons.append("crypto mining workload behavior")

    if reasons:
        return "AI detected abnormal cloud behavior due to " + ", ".join(reasons) + "."

    return "AI detected abnormal cloud behavior based on combined resource usage patterns."
results = []

for i, (_, row) in enumerate(sample.iterrows()):
    is_anomaly = int(predictions[i]) == 1
    probability = round(float(probabilities[i]), 4)

    results.append({
        "pack_name": "ai_cloud_anomaly_prediction",
        "service": row["Workload_Type"],
        "namespace": "ai-inference",
        "problem_type": "ai_predicted_cloud_anomaly",
        "severity": "high" if probability >= 0.8 else "medium" if probability >= 0.5 else "normal",
        "confidence": probability,
        "detected": is_anomaly,
        "explanation": build_explanation(is_anomaly, row),
        "evidence": {
            "cpu_usage": float(row["CPU_Usage"]),
            "memory_usage": float(row["Memory_Usage"]),
            "disk_io": float(row["Disk_IO"]),
            "network_io": float(row["Network_IO"]),
            "hour": int(row["hour"]),
            "day": int(row["day"]),
            "day_of_week": int(row["day_of_week"]),
            "anomaly_probability": probability
        },
        "recommendation": {
            "root_cause": "AI model detected abnormal cloud resource behavior." if is_anomaly else "No abnormal cloud resource behavior detected.",
            "recommendation": "Investigate workload resource usage and possible cost impact." if is_anomaly else "No action required.",
            "estimated_daily_savings": 0,
            "automation_candidate": False,
            "requires_approval": True
        },
        "automation": {
            "can_automate": False,
            "risk_level": "medium" if is_anomaly else "low",
            "requires_approval": True
        }
    })

with open(output_file, "w") as file:
    json.dump(results, file, indent=2)

print(f"Loaded input from {input_file}")
print(f"Saved {len(results)} AI predictions to {output_file}")