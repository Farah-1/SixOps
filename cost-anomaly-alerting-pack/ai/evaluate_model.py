import json
import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)

MODEL_FILE = "cost-anomaly-alerting-pack/ai/models/random_forest_anomaly_model.pkl"
DATA_FILE = "cost-anomaly-alerting-pack/ai/processed/clean_cloud_dataset.csv"
OUTPUT_FILE = "cost-anomaly-alerting-pack/ai/output/final_model_evaluation.json"

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

target = "Anomaly_Label"

df = pd.read_csv(DATA_FILE)
model = joblib.load(MODEL_FILE)

split_index = int(len(df) * 0.8)

test_df = df.iloc[split_index:].copy()

X_test = test_df[features]
y_test = test_df[target]

predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

evaluation = {
    "evaluation_type": "time_based_unseen_test",
    "test_rows": len(test_df),
    "accuracy": accuracy_score(y_test, predictions),
    "precision": precision_score(y_test, predictions),
    "recall": recall_score(y_test, predictions),
    "f1_score": f1_score(y_test, predictions),
    "roc_auc": roc_auc_score(y_test, probabilities),
    "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
    "classification_report": classification_report(y_test, predictions, output_dict=True),
}

print("Final AI Model Evaluation")
print("-------------------------")
print(f"Test rows: {evaluation['test_rows']}")
print(f"Accuracy: {evaluation['accuracy']:.4f}")
print(f"Precision: {evaluation['precision']:.4f}")
print(f"Recall: {evaluation['recall']:.4f}")
print(f"F1 Score: {evaluation['f1_score']:.4f}")
print(f"ROC AUC: {evaluation['roc_auc']:.4f}")
print("\nConfusion Matrix")
print(confusion_matrix(y_test, predictions))
print("\nClassification Report")
print(classification_report(y_test, predictions))

with open(OUTPUT_FILE, "w") as file:
    json.dump(evaluation, file, indent=2)

print(f"\nSaved evaluation to {OUTPUT_FILE}")