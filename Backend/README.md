# POL Backend

## تهيئة قاعدة البيانات للمطورين الجدد (Database Setup)

عند سحب الكود لأول مرة، تكون قاعدة البيانات فارغة وتحتاج إلى إعداد الجداول (Migrations) وزرع البيانات الثابتة (Seeders) مثل الرتب، الوظائف، ونظام الصلاحيات.

قمنا بتجهيز سكريبت `init_db.sh` يقوم بكل هذا تلقائياً بخطوة واحدة.

### 1️⃣ للمطورين الذين يستخدمون (Local Environment بدون Docker)
تأكد من تفعيل البيئة الوهمية (Virtual Environment) ثم قم بتشغيل:

```bash
bash init_db.sh
```

### 2️⃣ للمطورين الذين يستخدمون (Docker)
بعد تشغيل الحاويات باستخدام `docker-compose up -d`، قم بتنفيذ السكريبت داخل حاوية الباك-إند:

```bash
docker exec -it hrms_backend bash init_db.sh
```
*(ملاحظة: استبدل `hrms_backend` باسم الحاوية الخاص بك إذا كان مختلفاً)*

---

### ماذا يفعل هذا السكريبت؟
1. `python manage.py migrate`: ينشئ جميع جداول قاعدة البيانات.
2. `python manage.py seed_all_dictionaries`: يزرع القواميس الأساسية (الرتب، الحالات الخدمية، المسميات الوظيفية...).
3. `python manage.py seed_geography`: يزرع الهيكل الجغرافي للمحافظات.
4. `python manage.py seed_permissions`: يزرع نظام الصلاحيات بالكامل ويُعيّنها للأدوار.
5. `python manage.py loaddata ...`: يُحمل الأدوار الافتراضية (Super Admin, etc...).
