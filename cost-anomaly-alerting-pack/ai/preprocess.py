import os
import pandas as pd

RAW_DATA_FILE = "cost-anomaly-alerting-pack/ai/data/cloud_dataset.csv"
OUTPUT_DIR = "cost-anomaly-alerting-pack/ai/processed"
OUTPUT_FILE = f"{OUTPUT_DIR}/clean_cloud_dataset.csv"

df = pd.read_csv(RAW_DATA_FILE)

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

df["hour"] = df["Timestamp"].dt.hour
df["day"] = df["Timestamp"].dt.day
df["day_of_week"] = df["Timestamp"].dt.dayofweek

# Resource usage cannot be negative, so we clip negative values to zero.
resource_columns = [
    "CPU_Usage",
    "Memory_Usage",
    "Disk_IO",
    "Network_IO",
]

for column in resource_columns:
    df[column] = df[column].clip(lower=0)

# User_ID is removed to avoid user-specific overfitting.
df = df.drop(columns=["User_ID"])

os.makedirs(OUTPUT_DIR, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print("Preprocessing completed.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved clean dataset to {OUTPUT_FILE}")