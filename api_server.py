from fastapi import FastAPI
import subprocess
import json
import uvicorn
import sys
import os
from pathlib import Path
import json  # تأكدي من عمل Import لهذه المكتبة
# إضافة المجلد الرئيسي للمشروع إلى مسارات البحث
BASE_DIR = Path(__file__).resolve().parent
app = FastAPI()

# 1. تشغيل الأوبتيميزر
@app.post("/run-optimizer")
def run_optimizer():
    try:
        raw_output = subprocess.check_output(["python3", os.path.join(BASE_DIR,"optimizer/optimizer_manager.py")], text=True)
        data = json.loads(raw_output)
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 2. تحديث الميموري (موجود مسبقاً)
@app.post("/update-memory")
def update_memory(new_memory: str):
    cmd = ["ansible-playbook", "ansible/update_memory.yml", "-e", f"new_memory={new_memory}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {"status": "success", "output": result.stdout}

# 3. تحديث الريبلكا (موجود مسبقاً)
@app.post("/update-replicas")
def update_replicas(new_replicas: int):
    cmd = ["ansible-playbook", "ansible/update_replicas.yml", "-e", f"new_replicas={new_replicas}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {"status": "success", "output": result.stdout}

# 4. التحديث الجديد للـ CPU
@app.post("/update-cpu")
def update_cpu(new_cpu: str):
    # نستخدم نفس منطق الـ memory مع تغيير ملف البلايبوك
    cmd = ["ansible-playbook", "ansible/update_cpu.yml", "-e", f"new_cpu={new_cpu}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {"status": "success", "output": result.stdout}

# 5. التحديث الجديد للـ Storage
@app.post("/update-storage")
def update_storage(new_storage: str):
    # نمرر قيمة التخزين الجديدة
    cmd = ["ansible-playbook", "ansible/update_storage.yml", "-e", f"new_storage={new_storage}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {"status": "success", "output": result.stdout}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)