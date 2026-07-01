# 🔧 HRMS Backend

نظام إدارة القوى البشرية - Backend (Django)

## 🏗️ البنية

```
backend/
├── hrms/              # المشروع الرئيسي
│   ├── settings.py    # الإعدادات
│   ├── urls.py        # المسارات
│   └── celery.py      # Celery config
├── core/              # القواميس الأساسية
├── personnel/         # إدارة الأفراد
├── services/          # الخدمات والأحداث
└── manage.py
```

## 📦 التطبيقات (Apps)

### 1. Core (القواميس)
- Location, Rank, ServiceStatus
- JobCategory, JobTitle
- Qualification, Department

### 2. Personnel (الأفراد)
- PersonnelMaster (الملف الأساسي)

### 3. Services (الخدمات)
- Document, ServiceEventLog
- AuditLog, StagingRecord
- ReconciliationTask, MonthlySnapshot

## 🚀 التشغيل

### Development
```bash
# تشغيل الخادم
docker compose up -d backend

# Migrations
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate

# إنشاء superuser
docker compose exec backend python manage.py createsuperuser

# Django shell
docker compose exec backend python manage.py shell
```

### الوصول
- **API:** http://localhost:8000
- **Admin:** http://localhost:8000/admin
- **Swagger:** http://localhost:8000/swagger

## 🔧 الأوامر المفيدة

```bash
# عرض حالة migrations
docker compose exec backend python manage.py showmigrations

# التحقق من النماذج
docker compose exec backend python manage.py check

# إنشاء app جديد
docker compose exec backend python manage.py startapp app_name

# تشغيل tests
docker compose exec backend pytest

# Code formatting
docker compose exec backend black .
docker compose exec backend isort .
```

## 📊 قاعدة البيانات

- **Engine:** PostgreSQL 16
- **Database:** hrms_db
- **User:** hrms_user
- **Port:** 5432

## 🔐 الأمان

- JWT Authentication
- Permission-based access
- Audit logging
- Document integrity (SHA-256)
- Encrypted sensitive data

## 📝 التوثيق

- [PHASE1_COMPLETE.md](./PHASE1_COMPLETE.md) - المرحلة 1
- Swagger UI: http://localhost:8000/swagger
- ReDoc: http://localhost:8000/redoc

## 🧪 الاختبار

```bash
# تشغيل جميع الاختبارات
docker compose exec backend pytest

# تشغيل اختبارات محددة
docker compose exec backend pytest tests/test_personnel.py

# مع coverage
docker compose exec backend pytest --cov
```

## 📦 المكتبات الرئيسية

- Django 5.0
- Django REST Framework
- PostgreSQL (psycopg2)
- Redis
- Celery
- django-fsm (State Machine)
- django-guardian (Permissions)
- Pillow (Image processing)
