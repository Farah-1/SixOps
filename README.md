# 🚀 SixOps Optimization System

هذا النظام يقوم بمراقبة وتحسين الموارد (CPU, Memory, Storage) الخاصة بـ Kubernetes Deployment تلقائياً باستخدام Prometheus و n8n.

## 📋 المتطلبات (Prerequisites)
قبل البدء، تأكدي من تثبيت الأدوات التالية:
- Python 3.x
- Kubernetes CLI (`kubectl`)
- [ngrok](https://ngrok.com/download)
- Node.js & npm (لتشغيل n8n)

---

## 🛠 خطوات التشغيل (Run Instructions)

اتبعي هذه الخطوات بالترتيب، وافتحي "Terminal" منفصلة لكل عملية:

### 1. تشغيل الـ API
تشغيل السيرفر المسؤول عن استقبال طلبات التعديل:
```bash
python3 api_server.py
```
### 2. تشغيل اتصال Prometheus
للسماح للنظام بقراءة بيانات الأداء:
```bash
kubectl port-forward svc/prometheus-server 46691:80 -n monitoring
```
### 3. إعداد وتشغيل Ngrok
بعد تحميل ngrok وتثبيته، قومي بتشغيل الـ Tunnel على منفذ n8n:
```bash
# تسجيل الـ Token (مرة واحدة فقط)
ngrok config add-authtoken <YOUR_AUTH_TOKEN>

# تشغيل الـ Tunnel
ngrok http 5678
```
### 4. ضبط البيئة وتشغيل n8n
في terminal جديدة، قومي بضبط رابط الـ Webhook ثم شغلي n8n:
```bash
# ضعي الرابط الذي نسختِه من ngrok هنا
export WEBHOOK_URL=https://<YOUR_NGROK_URL>

# تشغيل n8n باستخدام npx
npx n8n start
```

### 5. الوصول للنظام
بعد تشغيل n8n، يمكنكِ الدخول إلى لوحة التحكم من المتصفح عبر الرابط:
👉 http://localhost:5678

💡 ملاحظات إضافية
Persistence: تأكدي أن kubectl متصل بـ Cluster فعال قبل تشغيل الـ API.

Environment: إذا كنتِ تستخدمين Virtual Environment للبايثون، لا تنسي تفعيلها (source venv/bin/activate) قبل الخطوة الأولى.

Troubleshooting: إذا واجهتِ مشكلة في الاتصال بـ Prometheus، تأكدي أن الـ Terminal الخاصة بالخطوة (2) لا تزال مفتوحة.
