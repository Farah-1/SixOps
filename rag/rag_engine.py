import os
from google import genai
import time

def generate_alert_message(data):
    client = genai.Client(api_key="AQ.Ab8RN6JmNQ_bYLfN_rOUYn2Dk5qkv4SY880WJ-PoMT5Epe_zjA")
    
    prompt = f"""
        بصفتك خبير DevOps، قدم ملخصاً تنفيذياً سريعاً:
        - الوضع الحالي: ميموري {data['current_memory']:.2f}Gi، CPU {data['current_cpu']:.0f}m، {data['current_replicas']} ريبلكا.
        - التوصية: ميموري {data['recommended_mem']:.2f}Gi، CPU {data['recommended_cpu']:.0f}m، {data['recommended_replicas']} ريبلكا.
        
        تنبيه تحسين موارد:
        1. الهدف: { "توفير التكاليف" if data['total_saving'] > 0 else "تعزيز استقرار الأداء" }.
        2. التغيير: ضبط الموارد لكل نسخة وعدد النسخ.
        3. النتيجة: { "توفير مالي يقدر بـ $" + str(round(data['total_saving'], 2)) if data['total_saving'] > 0 else "استثمار لضمان الجودة" }.
        
        هل توافق على التطبيق؟
        """
    
    max_retries = 10
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            return response.text

        except Exception as e:
            last_error = str(e)
          

            if "401" in last_error or "UNAUTHENTICATED" in last_error:
                return "❌ خطأ API KEY: تحقق من Google API Key"

            if attempt == max_retries:
                return f"فشل بعد 10 محاولات: {last_error}"

            time.sleep(5)