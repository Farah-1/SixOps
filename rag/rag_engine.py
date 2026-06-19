from google import genai
import time

def generate_alert_message(current, recommended):
    client = genai.Client(api_key="AQ.Ab8RN6IXEsK9ldbgdkP7gDM5tFZHS6sBWJk_WhtiF4kLg0B53g")
    
    prompt = f"""
    بصفتك خبير DevOps، قدم ملخصاً تنفيذياً سريعاً للتعديل المقترح.
    الوضع الحالي: الميموري {current['mem']}، الريبلكا {current['replicas']}.
    التوصية: الميموري {recommended['mem']}، الريبلكا {recommended['replicas']}.
    
    اكتب التنبيه في نقاط محددة:
    1. الهدف (الأداء vs التكلفة).
    2. التغيير المطلوب.
    3. النتيجة المتوقعة (لماذا هذا أفضل؟).
    
    ابدأ بـ "تنبيه تحسين موارد:" ولا تزيد عن 5 أسطر إجمالاً.
    انتهِ بـ "هل توافق على التطبيق؟".
    """
    
    max_retries = 10
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            return response.text
        except Exception as e:
            print(f"محاولة {attempt}/{max_retries} فشلت بسبب ضغط السيرفر...")
            if attempt == max_retries:
                return f"تعذر توليد التقرير بعد 10 محاولات. الخطأ الأخير: {e}"
            time.sleep(5)  # انتظار 5 ثواني قبل المحاولة التالية
