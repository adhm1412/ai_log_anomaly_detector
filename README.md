# AI Log Anomaly Detector
isolation forest
سكربت بايثون متقدم لحماية السيرفرات والشبكات عبر تحليل سجلات النظام (Logs) تلقائياً وكشف الحركات المشبوهة والهجمات غير المعروفة، بالاعتماد على خوارزمية التعلم غير الخاضع للإشراف



# الميزات الأساسية
Intrusion Detection كشف فوري للهجمات دون الحاجة لكتابة قواعد يدوية (Rules) أو الاعتماد على توقيعات الاختراق التقليدية
Feature Scaling دمج أداة Standard Scaler لتوحيد مقاييس الأرقام، مما يضمن دقة الفحص ومساواة الوزن الرياضي بين محاولات الاختراق وحجم البيانات المنقولة.
Production Logging استخدام نظام الـ `Logging` الرسمي للينكس لتوثيق العمليات بالوقت والتاريخ بدلاً من أوامر الطباعة العادية
Forensics Export فلترة التهديدات وعزلها تلقائياً وتصديرها في تقرير حوادث مستقل بصيغة CSV



# الهجمات التي تكشفها الأداة
يقوم النموذج بتحليل السلوك الشاذ وعزل الـ IPs المهاجمة بناءً على المعايير التالية:
1. Brute Force Attacks رصد القفزات غير الطبيعية في عدد محاولات الدخول الفاشلة ("failed_logins")
2. Port Scanning / Reconnaissance التقاط الارتفاع الهجومي المكثف في معدل الطلبات في الدقيقة (requests_per_minute)
3. Data Exfiltration كشف عمليات تسريب وسرقة البيانات حية عند قيام جهاز بسحب كميات هائلة ومفاجئة بالميجابايت (data_transferred_mb)



# هيكلية ملفات المستودع
bash
detector.py          محرك الفحص والذكاء الاصطناعي الرئيسي (OOP Architecture)
network_logs.csv     ملف التغذية وسجلات الشبكة (يحتوي على حركات طبيعية وهجمات)
detected_threats.csv  تقرير الحوادث السيبرانية المستخرج والمصفى تلقائياً

# التشغيل usage



عند تشغيل السكربت على بيئة لينكس، يقوم بطباعة التقرير الأمني الفوري التالي على الـ Terminal:

bash
INFO:root:Successfully ingested 8 log entries.
INFO:root:Training Isolation Forest engine...
WARNING:root:CRITICAL: Found 2 anomalies!

======================================================================
[!] ANOMALOUS TRAFFIC DETECTED (IMMEDIATE ACTION REQUIRED)
======================================================================
      ip_address  failed_logins  data_transferred_mb  requests_per_minute
3     10.0.0.25             20                    5                 1200
5  198.51.100.42              0                 8500                   10
======================================================================

INFO:root:Report saved to 'detected_threats.csv'.



Developed by adhm1412 

