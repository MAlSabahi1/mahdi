# توثيق APIs السجلات - Logs API Documentation

> **Base URL:** `/api/d-services/`  
> **التاريخ:** 2025-12-31

---

## جدول المحتويات

1. [ServiceLogsMVS - سجلات الخدمات](#1-servicelogsmvs---سجلات-الخدمات)
2. [RequestLogsMVS - سجلات الطلبات](#2-requestlogsmvs---سجلات-الطلبات)
3. [WorkflowLogsMVS - سجلات سير العمل](#3-workflowlogsmvs---سجلات-سير-العمل)

---

## 1. ServiceLogsMVS - سجلات الخدمات

**Base URL:** `/api/d-services/service-logs/`

### 1.1 list - قائمة السجلات

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /service-logs/` |
| **الوصف** | عرض قائمة سجلات الخدمات مع فلاتر متقدمة |
| **الاستخدام في الشاشة** | صفحة سجلات الخدمات الرئيسية، جدول يعرض جميع أحداث الخدمات |

**Query Parameters:**
```
fk_service         - معرف الخدمة
action             - نوع الإجراء (exact, in)
fk_user            - معرف المستخدم
severity           - مستوى الأهمية (INFO, WARNING, ERROR, CRITICAL)
is_flagged         - معلم (true/false)
reviewed_at__isnull - تمت المراجعة
timestamp__gte     - من تاريخ
timestamp__lte     - إلى تاريخ
search             - بحث في الملاحظات، كود الخدمة، اسم المستخدم
```

**Response:**
```json
{
    "success": true,
    "message": "تم جلب السجلات بنجاح",
    "data": [
        {
            "id": 1,
            "fk_service": 5,
            "fk_service__code": "SRV001",
            "fk_service__name_ar": "خدمة الإعفاء",
            "action": "CREATE",
            "action_display": "إنشاء",
            "fk_user": 10,
            "fk_user__username": "admin",
            "timestamp": "2025-12-31T10:30:00Z",
            "severity": "INFO",
            "notes": "تم إنشاء الخدمة",
            "is_flagged": false,
            "reviewed_at": null
        }
    ]
}
```

---

### 1.2 retrieve - تفاصيل سجل

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /service-logs/{id}/` |
| **الوصف** | عرض تفاصيل سجل معين |
| **الاستخدام في الشاشة** | نافذة تفاصيل السجل، عرض كامل البيانات والتغييرات |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب تفاصيل السجل بنجاح",
    "data": {
        "id": 1,
        "fk_service": 5,
        "fk_service__code": "SRV001",
        "fk_service__name_ar": "خدمة الإعفاء",
        "action": "UPDATE",
        "action_display": "تعديل",
        "fk_user": 10,
        "fk_user__username": "admin",
        "fk_user__full_name": "أحمد محمد",
        "timestamp": "2025-12-31T10:30:00Z",
        "severity": "INFO",
        "notes": "تم تعديل رسوم الخدمة",
        "changes": {
            "base_fee": {"old": 100, "new": 150}
        },
        "is_flagged": true,
        "flag_reason": "مراجعة مطلوبة",
        "reviewed_by": null,
        "reviewed_at": null,
        "review_notes": null
    }
}
```

---

### 1.3 by_service - سجلات خدمة معينة

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /service-logs/by_service/` |
| **الوصف** | جلب آخر سجلات خدمة معينة |
| **الاستخدام في الشاشة** | صفحة تفاصيل الخدمة - تاب السجلات |

**Query Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `service_id` | ✅ | - | معرف الخدمة |
| `limit` |  | 50 | عدد السجلات |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب سجلات الخدمة بنجاح",
    "data": [...],
    "count": 25
}
```

---

### 1.4 timeline - الجدول الزمني للخدمة

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /service-logs/timeline/` |
| **الوصف** | عرض timeline للأحداث مجمعة حسب التاريخ |
| **الاستخدام في الشاشة** | عرض Timeline في صفحة الخدمة |

**Query Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `service_id` | ✅ | معرف الخدمة |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب timeline الخدمة بنجاح",
    "data": [
        {
            "date": "2025-12-31",
            "events": [
                {
                    "id": 1,
                    "time": "10:30",
                    "action": "CREATE",
                    "action_display": "إنشاء",
                    "user": "admin",
                    "severity": "INFO",
                    "notes": "تم إنشاء الخدمة",
                    "is_flagged": false
                }
            ]
        }
    ]
}
```

---

### 1.5 statistics - الإحصائيات

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /service-logs/statistics/` |
| **الوصف** | إحصائيات شاملة للسجلات |
| **الاستخدام في الشاشة** | لوحة الإحصائيات، الرسوم البيانية |

**Query Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `service_id` |  | - | معرف الخدمة (اختياري) |
| `days` |  | 30 | عدد الأيام |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب الإحصائيات بنجاح",
    "data": {
        "total_count": 150,
        "flagged_count": 5,
        "pending_review_count": 3,
        "by_action": {
            "CREATE": {"count": 20, "display": "إنشاء"},
            "UPDATE": {"count": 100, "display": "تعديل"},
            "DELETE": {"count": 10, "display": "حذف"}
        },
        "by_severity": {
            "INFO": {"count": 120, "display": "معلومات"},
            "WARNING": {"count": 25, "display": "تحذير"},
            "ERROR": {"count": 5, "display": "خطأ"}
        },
        "by_day": [
            {"date": "2025-12-25", "count": 15},
            {"date": "2025-12-26", "count": 22}
        ]
    }
}
```

---

### 1.6 add_note - إضافة ملاحظة

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `POST /service-logs/{id}/add_note/` |
| **الوصف** | إضافة ملاحظة للسجل |
| **الاستخدام في الشاشة** | زر "إضافة ملاحظة" في تفاصيل السجل |

**Request Body:**
```json
{
    "note": "نص الملاحظة",
    "append": true
}
```

**Response:**
```json
{
    "success": true,
    "message": "تمت إضافة الملاحظة بنجاح",
    "data": {
        "notes": "[2025-12-31 10:30] admin: نص الملاحظة"
    }
}
```

---

### 1.7 flag - تعليم السجل

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `POST /service-logs/{id}/flag/` |
| **الوصف** | تعليم السجل للانتباه والمراجعة |
| **الاستخدام في الشاشة** | زر 🚩 في جدول السجلات |

**Request Body:**
```json
{
    "reason": "سبب التعليم (اختياري)"
}
```

**Response:**
```json
{
    "success": true,
    "message": "تم تعليم السجل بنجاح",
    "data": {
        "is_flagged": true,
        "flag_reason": "سبب التعليم"
    }
}
```

---

### 1.8 unflag - إزالة التعليم

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `POST /service-logs/{id}/unflag/` |
| **الوصف** | إزالة تعليم السجل |
| **الاستخدام في الشاشة** | زر إزالة التعليم |

**Response:**
```json
{
    "success": true,
    "message": "تمت إزالة تعليم السجل بنجاح",
    "data": {"is_flagged": false}
}
```

---

### 1.9 mark_reviewed - تعليم كمراجع

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `POST /service-logs/{id}/mark_reviewed/` |
| **الوصف** | تعليم السجل كتم المراجعة |
| **الاستخدام في الشاشة** | زر "تم المراجعة" ✅ |

**Request Body:**
```json
{
    "notes": "ملاحظات المراجعة (اختياري)"
}
```

**Response:**
```json
{
    "success": true,
    "message": "تم تعليم السجل كمراجع بنجاح",
    "data": {
        "reviewed_by": "admin",
        "reviewed_at": "2025-12-31T11:00:00Z",
        "review_notes": "تم التحقق"
    }
}
```

---

### 1.10 alerts - التنبيهات النشطة

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /service-logs/alerts/` |
| **الوصف** | السجلات المعلمة غير المراجعة |
| **الاستخدام في الشاشة** | أيقونة التنبيهات 🔔 في الهيدر |

**Query Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `service_id` |  | معرف الخدمة (اختياري) |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب التنبيهات بنجاح",
    "data": [...],
    "count": 3
}
```

---

### 1.11 flagged - السجلات المعلمة

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /service-logs/flagged/` |
| **الوصف** | جميع السجلات المعلمة |
| **الاستخدام في الشاشة** | فلتر "المعلمة فقط" |

**Query Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `service_id` |  | معرف الخدمة (اختياري) |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب السجلات المعلمة بنجاح",
    "data": [...],
    "count": 10
}
```

---

### 1.12 critical - السجلات الحرجة

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /service-logs/critical/` |
| **الوصف** | سجلات ERROR و CRITICAL فقط |
| **الاستخدام في الشاشة** | تاب "الحرجة" في السجلات |

**Query Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `service_id` |  | - | معرف الخدمة |
| `days` |  | 7 | عدد الأيام |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب السجلات الحرجة بنجاح",
    "data": [...],
    "count": 2
}
```

---

### 1.13 export - تصدير السجلات

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /service-logs/export/` |
| **الوصف** | تصدير السجلات كـ JSON |
| **الاستخدام في الشاشة** | زر "تصدير" 📥 |

**Query Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `service_id` |  | - | معرف الخدمة |
| `days` |  | 30 | عدد الأيام |

**Response:**
```json
{
    "success": true,
    "message": "تم تصدير السجلات بنجاح",
    "data": [
        {
            "id": 1,
            "service_code": "SRV001",
            "action": "CREATE",
            "action_display": "إنشاء",
            "user": "admin",
            "timestamp": "2025-12-31T10:30:00+00:00",
            "severity": "INFO",
            "notes": "...",
            "is_flagged": false,
            "changes": {}
        }
    ],
    "count": 150
}
```

---

## 2. RequestLogsMVS - سجلات الطلبات

**Base URL:** `/api/d-services/request-logs/`

### 2.1 list - قائمة سجلات الطلبات

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /request-logs/` |
| **الوصف** | عرض سجلات جميع الطلبات |
| **الاستخدام في الشاشة** | صفحة سجلات الطلبات الرئيسية |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب سجلات الطلبات بنجاح",
    "data": [
        {
            "id": 1,
            "fk_request": 100,
            "fk_request__request_number": "REQ-000001",
            "fk_request__fk_service__name_ar": "خدمة الإعفاء",
            "action": "STATUS_CHANGE",
            "action_display": "تغيير الحالة",
            "fk_user": 10,
            "fk_user__username": "admin",
            "timestamp": "2025-12-31T10:30:00Z",
            "severity": "INFO",
            "old_status": "PENDING",
            "new_status": "IN_PROGRESS",
            "notes": "تم بدء معالجة الطلب",
            "is_flagged": false
        }
    ]
}
```

---

### 2.2 by_request - سجلات طلب معين

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /request-logs/by_request/` |
| **الوصف** | جلب سجلات طلب محدد |
| **الاستخدام في الشاشة** | صفحة تفاصيل الطلب - تاب السجلات |

**Query Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `request_id` | ✅ | - | معرف الطلب |
| `limit` |  | 50 | عدد السجلات |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب سجلات الطلب بنجاح",
    "data": [...]
}
```

---

### 2.3 timeline - الجدول الزمني للطلب

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /request-logs/timeline/` |
| **الوصف** | عرض timeline شامل (Request + Workflow logs) |
| **الاستخدام في الشاشة** | عرض Timeline الكامل للطلب |

**Query Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `request_id` | ✅ | معرف الطلب |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب timeline الطلب بنجاح",
    "data": [
        {
            "date": "2025-12-31",
            "events": [
                {
                    "type": "request",
                    "id": 1,
                    "time": "10:30",
                    "action": "CREATE",
                    "action_display": "إنشاء",
                    "user": "student1",
                    "severity": "INFO",
                    "old_status": null,
                    "new_status": "PENDING",
                    "notes": "تم تقديم الطلب",
                    "is_flagged": false
                },
                {
                    "type": "workflow",
                    "id": 5,
                    "time": "11:00",
                    "action": "STAGE_START",
                    "action_display": "بدء المرحلة",
                    "user": "admin",
                    "from_stage": null,
                    "to_stage": "المراجعة الأولية",
                    "action_taken": "بدء",
                    "severity": "INFO",
                    "sla_status": "ON_TIME",
                    "is_overdue": false,
                    "notes": null
                }
            ]
        }
    ]
}
```

---

### 2.4 status_changes - تغييرات الحالة

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /request-logs/status_changes/` |
| **الوصف** | تتبع تغييرات حالة الطلب |
| **الاستخدام في الشاشة** | مؤشر تدفق الحالة (Status Flow) |

**Query Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `request_id` | ✅ | معرف الطلب |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب تغييرات الحالة بنجاح",
    "data": [
        {
            "id": 1,
            "timestamp": "2025-12-31T10:30:00Z",
            "old_status": null,
            "new_status": "PENDING",
            "user": "student1",
            "notes": "تم إنشاء الطلب"
        },
        {
            "id": 2,
            "timestamp": "2025-12-31T11:00:00Z",
            "old_status": "PENDING",
            "new_status": "IN_PROGRESS",
            "user": "admin",
            "notes": "تم بدء المعالجة"
        }
    ]
}
```

---

### 2.5 statistics - إحصائيات سجلات الطلبات

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /request-logs/statistics/` |
| **الوصف** | إحصائيات شاملة لسجلات الطلبات |
| **الاستخدام في الشاشة** | لوحة الإحصائيات |

**Query Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `days` |  | 30 | عدد الأيام |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب الإحصائيات بنجاح",
    "data": {
        "total_count": 500,
        "flagged_count": 10,
        "by_action": {
            "CREATE": 100,
            "STATUS_CHANGE": 300,
            "UPDATE": 100
        },
        "by_status_change": [
            {"old_status": "PENDING", "new_status": "IN_PROGRESS", "count": 150},
            {"old_status": "IN_PROGRESS", "new_status": "COMPLETED", "count": 120}
        ]
    }
}
```

---

### 2.6 add_note - إضافة ملاحظة

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `POST /request-logs/{id}/add_note/` |
| **الوصف** | إضافة ملاحظة للسجل |
| **الاستخدام في الشاشة** | زر "إضافة ملاحظة" |

**Request Body:**
```json
{
    "note": "نص الملاحظة"
}
```

**Response:**
```json
{
    "success": true,
    "message": "تمت إضافة الملاحظة بنجاح"
}
```

---

### 2.7 flag - تعليم السجل

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `POST /request-logs/{id}/flag/` |
| **الوصف** | تعليم السجل للانتباه |
| **الاستخدام في الشاشة** | زر 🚩 |

**Request Body:**
```json
{
    "reason": "سبب التعليم (اختياري)"
}
```

**Response:**
```json
{
    "success": true,
    "message": "تم تعليم السجل بنجاح"
}
```

---

### 2.8 alerts - التنبيهات

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /request-logs/alerts/` |
| **الوصف** | السجلات المعلمة |
| **الاستخدام في الشاشة** | أيقونة التنبيهات 🔔 |

**Query Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `request_id` |  | معرف الطلب (اختياري) |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب التنبيهات بنجاح",
    "data": [...]
}
```

---

## 3. WorkflowLogsMVS - سجلات سير العمل

**Base URL:** `/api/d-services/workflow-logs/`

### 3.1 list - قائمة سجلات سير العمل

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /workflow-logs/` |
| **الوصف** | عرض سجلات سير العمل |
| **الاستخدام في الشاشة** | صفحة سجلات سير العمل |

**Filter Fields:**
```
fk_request      - معرف الطلب
fk_user         - معرف المستخدم
action          - نوع الإجراء
sla_status      - حالة SLA (ON_TIME, AT_RISK, OVERDUE)
is_overdue      - متأخر (true/false)
is_flagged      - معلم (true/false)
timestamp       - التاريخ
```

**Response:**
```json
{
    "success": true,
    "message": "تم جلب سجلات سير العمل بنجاح",
    "data": [
        {
            "id": 1,
            "fk_request": 100,
            "fk_request__request_number": "REQ-000001",
            "action": "STAGE_COMPLETE",
            "action_display": "إكمال المرحلة",
            "from_stage_name": "المراجعة الأولية",
            "to_stage_name": "الموافقة",
            "action_taken": "موافقة",
            "fk_user__username": "admin",
            "timestamp": "2025-12-31T11:30:00Z",
            "sla_status": "ON_TIME",
            "actual_duration_hours": 1.5,
            "is_overdue": false
        }
    ]
}
```

---

### 3.2 by_request - سجلات سير العمل لطلب

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /workflow-logs/by_request/` |
| **الوصف** | سجلات سير العمل لطلب معين |
| **الاستخدام في الشاشة** | صفحة تفاصيل الطلب - تاب سير العمل |

**Query Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `request_id` | ✅ | معرف الطلب |

---

### 3.3 transitions - الانتقالات بين المراحل

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /workflow-logs/transitions/` |
| **الوصف** | تتبع الانتقالات بين المراحل |
| **الاستخدام في الشاشة** | رسم بياني لمسار الطلب |

**Query Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `request_id` | ✅ | معرف الطلب |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب الانتقالات بنجاح",
    "data": [
        {
            "id": 1,
            "timestamp": "2025-12-31T10:30:00Z",
            "from_stage": null,
            "to_stage": "المراجعة الأولية",
            "action": "STAGE_START",
            "action_taken": "بدء",
            "user": "admin",
            "duration_hours": null,
            "sla_status": "ON_TIME",
            "is_overdue": false
        },
        {
            "id": 2,
            "timestamp": "2025-12-31T12:00:00Z",
            "from_stage": "المراجعة الأولية",
            "to_stage": "الموافقة",
            "action": "STAGE_COMPLETE",
            "action_taken": "موافقة",
            "user": "admin",
            "duration_hours": 1.5,
            "sla_status": "ON_TIME",
            "is_overdue": false
        }
    ]
}
```

---

### 3.4 sla_report - تقرير SLA

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /workflow-logs/sla_report/` |
| **الوصف** | تقرير أداء SLA |
| **الاستخدام في الشاشة** | لوحة SLA Dashboard |

**Query Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `days` |  | 30 | عدد الأيام |
| `service_id` |  | - | معرف الخدمة |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب تقرير SLA بنجاح",
    "data": {
        "total": 100,
        "on_time": 85,
        "at_risk": 10,
        "overdue": 5,
        "on_time_percentage": 85.0,
        "avg_duration_hours": 2.5,
        "avg_overdue_hours": 0.5
    }
}
```

---

### 3.5 overdue - المراحل المتأخرة

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /workflow-logs/overdue/` |
| **الوصف** | قائمة المراحل المتأخرة |
| **الاستخدام في الشاشة** | تنبيهات المراحل المتأخرة ⚠️ |

**Query Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `request_id` |  | معرف الطلب (اختياري) |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب المراحل المتأخرة بنجاح",
    "data": [...],
    "count": 5
}
```

---

### 3.6 performance - تقرير الأداء

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /workflow-logs/performance/` |
| **الوصف** | تقرير أداء معالجة الطلب |
| **الاستخدام في الشاشة** | صفحة تحليل أداء الطلب |

**Query Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `request_id` | ✅ | معرف الطلب |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب تقرير الأداء بنجاح",
    "data": {
        "total_duration_hours": 24.5,
        "stages_count": 4,
        "completed_stages": 3,
        "on_time_count": 2,
        "overdue_count": 1,
        "avg_stage_duration": 6.125
    }
}
```

---

### 3.7 stage_stats - إحصائيات المرحلة

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `GET /workflow-logs/stage_stats/` |
| **الوصف** | إحصائيات أداء مرحلة معينة |
| **الاستخدام في الشاشة** | تحليل أداء المراحل |

**Query Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `stage_id` | ✅ | معرف المرحلة |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب إحصائيات المرحلة بنجاح",
    "data": {
        "total": 50,
        "avg_duration": 2.5,
        "max_duration": 8.0,
        "overdue_count": 3,
        "by_action": {
            "COMPLETE": 40,
            "REJECT": 5,
            "RETURN": 5
        }
    }
}
```

---

### 3.8 add_note - إضافة ملاحظة

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `POST /workflow-logs/{id}/add_note/` |
| **الوصف** | إضافة ملاحظة للسجل |
| **الاستخدام في الشاشة** | زر "إضافة ملاحظة" |

**Request Body:**
```json
{
    "note": "نص الملاحظة"
}
```

---

### 3.9 flag - تعليم السجل

| الحقل | القيمة |
|-------|--------|
| **Endpoint** | `POST /workflow-logs/{id}/flag/` |
| **الوصف** | تعليم السجل للانتباه |
| **الاستخدام في الشاشة** | زر 🚩 |

**Request Body:**
```json
{
    "reason": "سبب التعليم (اختياري)"
}
```

---

## ملخص الـ APIs

| MVS | عدد الـ APIs | الاستخدام |
|-----|-------------|-----------|
| **ServiceLogsMVS** | 13 | تتبع أحداث الخدمات |
| **RequestLogsMVS** | 8 | تتبع أحداث الطلبات |
| **WorkflowLogsMVS** | 9 | تتبع سير العمل وSLA |
| **الإجمالي** | **30** | - |

---

> **ملاحظة:** جميع الـ APIs تتطلب `Authorization: Bearer <token>` في الـ Header
