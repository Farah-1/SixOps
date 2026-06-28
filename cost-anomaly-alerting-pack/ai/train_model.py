import os
import json
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


DATA_FILE = "cost-anomaly-alerting-pack/ai/processed/clean_cloud_dataset.csv"
MODEL_DIR = "cost-anomaly-alerting-pack/ai/models"
OUTPUT_DIR = "cost-anomaly-alerting-pack/ai/output"

MODEL_FILE = f"{MODEL_DIR}/random_forest_anomaly_model.pkl"
REPORT_FILE = f"{OUTPUT_DIR}/model_evaluation.json"

df = pd.read_csv(DATA_FILE)

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

X = df[features]
y = df[target]

numeric_features = [
    "CPU_Usage",
    "Memory_Usage",
    "Disk_IO",
    "Network_IO",
    "hour",
    "day",
    "day_of_week",
]

categorical_features = ["Workload_Type"]

preprocessor = ColumnTransformer(
    transformers=[
        ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("numeric", "passthrough", numeric_features),
    ]
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
    max_depth=10,
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ]
)

# Time-based split to simulate future prediction
split_index = int(len(X) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

pipeline.fit(X_train, y_train)

predictions = pipeline.predict(X_test)
probabilities = pipeline.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, predictions)
report = classification_report(y_test, predictions, output_dict=True)
matrix = confusion_matrix(y_test, predictions).tolist()

feature_names = (
    list(
        pipeline.named_steps["preprocessor"]
        .named_transformers_["categorical"]
        .get_feature_names_out(categorical_features)
    )
    + numeric_features
)

importances = pipeline.named_steps["model"].feature_importances_

feature_importance = sorted(
    zip(feature_names, importances),
    key=lambda item: item[1],
    reverse=True
)

evaluation = {
    "model_name": "RandomForestClassifier",
    "validation_strategy": "time_based_split",
    "dataset_rows": len(df),
    "features": features,
    "target": target,
    "accuracy": accuracy,
    "classification_report": report,
    "confusion_matrix": matrix,
    "average_anomaly_probability": float(probabilities.mean()),
    "feature_importance": [
        {"feature": name, "importance": float(importance)}
        for name, importance in feature_importance
    ],
    "note": (
        "High accuracy is expected because the dataset contains clearly separable "
        "cloud anomaly patterns. Feature importance is used to verify that the model "
        "is relying on meaningful infrastructure signals."
    )
}

print("AI Model Training Report")
print("------------------------")
print(f"Rows: {len(df)}")
print(f"Features: {features}")
print(f"Target: {target}")
print(f"Accuracy: {accuracy:.4f}")

print("\nClassification Report")
print("---------------------")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix")
print("----------------")
print(confusion_matrix(y_test, predictions))

print("\nFeature Importance")
print("------------------")
for name, importance in feature_importance:
    print(f"{name}: {importance:.4f}")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

joblib.dump(pipeline, MODEL_FILE)

with open(REPORT_FILE, "w") as file:
    json.dump(evaluation, file, indent=2)

print(f"\nSaved model to {MODEL_FILE}")
print(f"Saved evaluation report to {REPORT_FILE}")