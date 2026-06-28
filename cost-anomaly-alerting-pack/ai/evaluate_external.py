import pandas as pd
import joblib
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

MODEL_FILE = "cost-anomaly-alerting-pack/ai/models/random_forest_anomaly_model.pkl"
DATA_FILE = "cost-anomaly-alerting-pack/ai/external_test.csv"

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

df = pd.read_csv(DATA_FILE)
model = joblib.load(MODEL_FILE)

X = df[features]
y = df["Expected_Label"]

predictions = model.predict(X)
probabilities = model.predict_proba(X)[:, 1]

df["Predicted_Label"] = predictions
df["Anomaly_Probability"] = probabilities.round(4)

print("External Validation Report")
print("--------------------------")
print(f"Rows: {len(df)}")
print(f"Accuracy: {accuracy_score(y, predictions):.4f}")

print("\nConfusion Matrix")
print(confusion_matrix(y, predictions))

print("\nClassification Report")
print(classification_report(y, predictions))

print("\nPredictions")
print(df[["CPU_Usage", "Memory_Usage", "Disk_IO", "Network_IO", "Workload_Type", "Expected_Label", "Predicted_Label", "Anomaly_Probability"]])