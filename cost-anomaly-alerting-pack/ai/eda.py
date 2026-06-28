import pandas as pd

DATA_FILE = "cost-anomaly-alerting-pack/ai/data/cloud_dataset.csv"

df = pd.read_csv(DATA_FILE)

print("REAL CLOUD DATASET EDA REPORT")
print("=============================")

print("\nDataset Shape")
print("-------------")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nColumns")
print("-------")
print(df.columns.tolist())

print("\nData Types")
print("----------")
print(df.dtypes)

print("\nMissing Values")
print("--------------")
print(df.isnull().sum())

print("\nDuplicate Rows")
print("--------------")
print(df.duplicated().sum())

print("\nTarget Distribution")
print("-------------------")
print(df["Anomaly_Label"].value_counts())
print(df["Anomaly_Label"].value_counts(normalize=True) * 100)

print("\nWorkload Type Distribution")
print("--------------------------")
print(df["Workload_Type"].value_counts())

print("\nBasic Statistics")
print("----------------")
print(df.describe())

print("\nAI Readiness Check")
print("------------------")
if df.isnull().sum().sum() == 0:
    print("PASS: No missing values.")
else:
    print("WARNING: Missing values found.")

if df.duplicated().sum() == 0:
    print("PASS: No duplicate rows.")
else:
    print("WARNING: Duplicate rows found.")

if df["Anomaly_Label"].nunique() == 2:
    print("PASS: Binary anomaly classification target found.")
else:
    print("WARNING: Target is not binary.")

print("EDA completed.")