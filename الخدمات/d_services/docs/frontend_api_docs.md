# وثائق API للخدمات الديناميكية - D_Services Frontend API Documentation

> **التاريخ:** 2025-12-29  
> **Base URL:** `/api/d-services/`

---

## جدول المحتويات

1. [Services (الخدمات)](#1-services-الخدمات)
2. [ServiceRequests (الطلبات)](#2-servicerequests-الطلبات)
3. [RequestActions (مراحل الطلبات)](#3-requestactions-مراحل-الطلبات)
4. [GrantSource (مصادر المنح)](#4-grantsource-مصادر-المنح)
5. [Permissions (الصلاحيات)](#5-permissions-الصلاحيات)
6. [ServiceLogs (سجلات الخدمات)](#6-servicelogs-سجلات-الخدمات)
7. [RequestLogs (سجلات الطلبات)](#7-requestlogs-سجلات-الطلبات)
8. [Logs (السجلات الأساسية)](#8-logs-السجلات-الأساسية)
9. [Verifications (التحققات)](#9-verifications-التحققات)
10. [Components (المكونات)](#10-components-المكونات)
11. [ExternalMethods (الدوال الخارجية)](#11-externalmethods-الدوال-الخارجية)

---

## 1. Services (الخدمات)

### Section Overview
| Field | Value |
|-------|-------|
| **اسم القسم بالعربي** | الخدمات |
| **Model** | `Service`, `ServiceVersion`, `OrganizationServiceConfig`, `ServiceInstallmentPlan`, `ServicePrerequisite`, `WorkflowStage`, `ServiceWorkflowStep` |
| **MVS** | `ServiceMVS`, `ServiceVersionMVS`, `OrganizationServiceConfigMVS`, `ServiceInstallmentPlanMVS`, `ServicePrerequisiteMVS`, `WorkflowStageMVS`, `ServiceWorkflowStepMVS` |
| **Base URL** | `/api/d-services/services/` |
| **Priority** | 🔴 Critical |
| **Status Field** | `is_active` |
| **Statuses** | `true`, `false` |
| **Permissions** | `ServicePermissionType` |

### ServiceMVS APIs

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 1 | `/services/` | GET | list | عرض قائمة الخدمات | - | - |
| 2 | `/services/{id}/` | GET | retrieve | عرض تفاصيل خدمة معينة | - | - |
| 3 | `/services/{id}/` | PATCH | partial_update | تعديل جزئي للخدمة | superuser | - |
| 4 | `/services/{id}/toggle-active/` | POST | toggle_active | تفعيل/إيقاف الخدمة | superuser | `is_active: true ↔ false` |

### ServiceVersionMVS APIs

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 5 | `/service-versions/` | GET | list | قائمة إصدارات الخدمة | - | - |
| 6 | `/service-versions/{id}/` | GET | retrieve | تفاصيل إصدار | - | - |
| 7 | `/service-versions/` | POST | create | إنشاء إصدار جديد | superuser | - |
| 8 | `/service-versions/{id}/` | PUT | update | تعديل إصدار | superuser | - |
| 9 | `/service-versions/{id}/` | PATCH | partial_update | تعديل جزئي للإصدار | superuser | - |
| 10 | `/service-versions/{id}/set-current/` | POST | set_current | تعيين كإصدار حالي | superuser | `is_current: false → true` |

### OrganizationServiceConfigMVS APIs

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 11 | `/organization-service-config/` | GET | list | قائمة تكوينات الخدمات | manager | - |
| 12 | `/organization-service-config/{id}/` | GET | retrieve | تفاصيل تكوين | manager | - |
| 13 | `/organization-service-config/` | POST | create | إنشاء تكوين | superuser | - |
| 14 | `/organization-service-config/{id}/` | PUT | update | تعديل تكوين | manager | - |
| 15 | `/organization-service-config/{service_pk}/activate-for-organizations/` | POST | activate_for_organizations | تفعيل الخدمة لجميع المنظمات | superuser | - |
| 16 | `/organization-service-config/{id}/toggle-lock/` | POST | toggle_lock | قفل/فتح التكوين | manager | `is_locked: true ↔ false` |

### ServiceInstallmentPlanMVS APIs

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 17 | `/service-installment-plans/` | GET | list | قائمة خطط الأقساط (Query: `fk_org_service_config`) | manager | - |
| 18 | `/service-installment-plans/` | POST | create | إنشاء/تحديث خطط الأقساط (Bulk sync) | manager | - |

### ServicePrerequisiteMVS APIs

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 19 | `/service-prerequisites/` | GET | list | قائمة المتطلبات المسبقة | - | - |
| 20 | `/service-prerequisites/{id}/` | GET | retrieve | تفاصيل متطلب | - | - |
| 21 | `/service-prerequisites/` | POST | create | إنشاء متطلب | superuser | - |

### WorkflowStageMVS APIs

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 22 | `/workflow-stages/` | GET | list | قائمة مراحل سير العمل | - | - |
| 23 | `/workflow-stages/{id}/` | GET | retrieve | تفاصيل مرحلة | - | - |

### ServiceWorkflowStepMVS APIs

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 24 | `/service-workflow-steps/` | GET | list | قائمة خطوات سير العمل | - | - |
| 25 | `/service-workflow-steps/{id}/` | GET | retrieve | تفاصيل خطوة | - | - |
| 26 | `/service-workflow-steps/` | POST | create | إنشاء خطوة جديدة | superuser | - |

---

## 2. ServiceRequests (الطلبات)

### Section Overview
| Field | Value |
|-------|-------|
| **اسم القسم بالعربي** | طلبات الخدمات |
| **Model** | `ServiceRequest` |
| **MVS** | `ServiceRequestMVS` |
| **Base URL** | `/api/d-services/service-requests/` |
| **Priority** | 🔴 Critical |
| **Status Field** | `status` |
| **Statuses** | `PENDING`, `IN_PROGRESS`, `COMPLETED`, `REJECTED`, `CANCELLED` |
| **Permissions** | `ServicePermissionType` (CREATE, READ, UPDATE, DELETE, PRINT, START, APPROVE, REJECT, LOCK, UNLOCK, CANCEL, COMPLETE, ASSIGN_GRANT, APPROVE_GRANT, UPDATE_GRANT, CANCEL_GRANT, REJECT_GRANT, ADD_DISCOUNT, APPROVE_DISCOUNT, UPDATE_DISCOUNT, CANCEL_DISCOUNT, REJECT_DISCOUNT, GET_INPUT_DATA, GET_OUTPUT_DATA, UPLOAD_INPUT, UPLOAD_OUTPUT, DELETE_INPUT, DELETE_OUTPUT) |

### ServiceRequestMVS APIs

#### CRUD Operations

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 1 | `/service-requests/` | GET | list | عرض قائمة الطلبات (Query: `fk_service`, `status`, `priority`, `payment_status`, etc.) | READ | - |
| 2 | `/service-requests/{id}/` | GET | retrieve | عرض تفاصيل طلب مع schema | READ | - |
| 3 | `/service-requests/` | POST | create | إنشاء طلب جديد | CREATE | → `PENDING` |
| 4 | `/service-requests/{id}/` | PUT | update | تعديل طلب | UPDATE | - |
| 5 | `/service-requests/{id}/` | PATCH | partial_update | تعديل جزئي للطلب | UPDATE | - |

#### Request Lifecycle

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 6 | `/service-requests/{id}/start-request/` | POST | start_request | بدء معالجة الطلب وإنشاء مراحل سير العمل | START | `PENDING → IN_PROGRESS` |
| 7 | `/service-requests/{id}/lock-request/` | POST | lock_request | قفل الطلب مع سبب | LOCK | `is_locked: false → true` |
| 8 | `/service-requests/{id}/unlock-request/` | POST | unlock_request | فتح الطلب | UNLOCK | `is_locked: true → false` |
| 9 | `/service-requests/{id}/reject-request/` | POST | reject_request | رفض الطلب مع سبب | REJECT | `* → REJECTED` |
| 10 | `/service-requests/{id}/complete-request/` | POST | complete_request | إكمال الطلب | COMPLETE | `IN_PROGRESS → COMPLETED` |
| 11 | `/service-requests/{id}/cancel-request/` | POST | cancel_request | إلغاء الطلب مع سبب | CANCEL | `* → CANCELLED` |

#### Grant Management

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 12 | `/service-requests/{id}/assign-grant/` | POST | assign_grant | تخصيص منحة للطلب | ASSIGN_GRANT | `grant_status: null → PENDING` |
| 13 | `/service-requests/{id}/approve-grant/` | POST | approve_grant | الموافقة على المنحة | APPROVE_GRANT | `grant_status: PENDING → APPROVED` |
| 14 | `/service-requests/{id}/update-grant/` | POST | update_grant | تحديث بيانات المنحة | UPDATE_GRANT | - |
| 15 | `/service-requests/{id}/cancel-grant/` | POST | cancel_grant | إلغاء المنحة | CANCEL_GRANT | `grant_status: * → CANCELLED` |
| 16 | `/service-requests/{id}/reject-grant/` | POST | reject_grant | رفض المنحة مع سبب | REJECT_GRANT | `grant_status: PENDING → REJECTED` |

#### Discount Management

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 17 | `/service-requests/{id}/add-discount/` | POST | add_discount | إضافة خصم للطلب | ADD_DISCOUNT | `discount_status: null → PENDING` |
| 18 | `/service-requests/{id}/approve-discount/` | POST | approve_discount | الموافقة على الخصم | APPROVE_DISCOUNT | `discount_status: PENDING → APPROVED` |
| 19 | `/service-requests/{id}/update-discount/` | POST | update_discount | تحديث بيانات الخصم | UPDATE_DISCOUNT | - |
| 20 | `/service-requests/{id}/cancel-discount/` | POST | cancel_discount | إلغاء الخصم | CANCEL_DISCOUNT | `discount_status: * → CANCELLED` |
| 21 | `/service-requests/{id}/reject-discount/` | POST | reject_discount | رفض الخصم مع سبب | REJECT_DISCOUNT | `discount_status: PENDING → REJECTED` |

#### Notes Management

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 22 | `/service-requests/{id}/list-notes/` | GET | list_notes | عرض ملاحظات الطلب | READ | - |
| 23 | `/service-requests/{id}/add-note/` | POST | add_note | إضافة ملاحظة | READ | - |
| 24 | `/service-requests/{id}/delete-note/{note_id}/` | DELETE | delete_note | حذف ملاحظة | owner/manager | - |

#### Document Management

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 25 | `/service-requests/{id}/get-input-data/` | GET | get_input_data | جلب بيانات المدخل | GET_INPUT_DATA | - |
| 26 | `/service-requests/{id}/get-output-data/` | GET | get_output_data | جلب بيانات المخرج | GET_OUTPUT_DATA | - |
| 27 | `/service-requests/{id}/upload-input/` | POST | upload_input | رفع ملف المدخل | UPLOAD_INPUT | - |
| 28 | `/service-requests/{id}/upload-output/` | POST | upload_output | رفع ملف المخرج | UPLOAD_OUTPUT | - |
| 29 | `/service-requests/{id}/delete-input/` | DELETE | delete_input | حذف ملف المدخل | DELETE_INPUT | - |
| 30 | `/service-requests/{id}/delete-output/` | DELETE | delete_output | حذف ملف المخرج | DELETE_OUTPUT | - |

---

## 3. RequestActions (مراحل الطلبات)

### Section Overview
| Field | Value |
|-------|-------|
| **اسم القسم بالعربي** | مراحل الطلبات |
| **Model** | `RequestAction` |
| **MVS** | `RequestActionMVS` |
| **Base URL** | `/api/d-services/request-actions/` |
| **Priority** | 🔴 Critical |
| **Status Field** | `status` |
| **Statuses** | `PENDING`, `IN_PROGRESS`, `COMPLETED`, `REJECTED`, `RETURNED`, `SKIPPED` |
| **Permissions** | `ActionPermissionType` (START, COMPLETE, APPROVE, REJECT, RETURN, ADVANCE, EXECUTE, INPUT, OUTPUT, NOTE) |

### RequestActionMVS APIs

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 1 | `/request-actions/` | GET | list | قائمة المراحل (Query: `fk_request`) | - | - |
| 2 | `/request-actions/{id}/` | GET | retrieve | تفاصيل مرحلة | - | - |
| 3 | `/request-actions/{id}/start-stage/` | POST | start_stage | بدء العمل على المرحلة | START (StagePermission) | `PENDING → IN_PROGRESS` |
| 4 | `/request-actions/{id}/complete-stage/` | POST | complete_stage | إكمال المرحلة | COMPLETE (StagePermission) | `IN_PROGRESS → COMPLETED` |
| 5 | `/request-actions/{id}/approve-stage/` | POST | approve_stage | الموافقة على المرحلة | APPROVE (StagePermission) | `IN_PROGRESS → COMPLETED` |
| 6 | `/request-actions/{id}/reject-stage/` | POST | reject_stage | رفض المرحلة | REJECT (StagePermission) | `IN_PROGRESS → REJECTED` |
| 7 | `/request-actions/{id}/return-stage/` | POST | return_stage | إرجاع المرحلة | RETURN (StagePermission) | `IN_PROGRESS → RETURNED` |
| 8 | `/request-actions/{id}/advance-to-next/` | POST | advance_to_next | الانتقال للمرحلة التالية | ADVANCE (StagePermission) | - |
| 9 | `/request-actions/{id}/execute-stage/` | POST | execute_stage | تنفيذ إجراء المرحلة | EXECUTE (StagePermission) | - |
| 10 | `/request-actions/{id}/get-input-template-data/` | GET | get_input_template_data | جلب بيانات قالب المدخل | INPUT (StagePermission) | - |
| 11 | `/request-actions/{id}/get-output-template-data/` | GET | get_output_template_data | جلب بيانات قالب المخرج | OUTPUT (StagePermission) | - |
| 12 | `/request-actions/{id}/upload-input/` | POST | upload_input | رفع ملف المدخل للمرحلة | INPUT (StagePermission) | - |
| 13 | `/request-actions/{id}/upload-output/` | POST | upload_output | رفع ملف المخرج للمرحلة | OUTPUT (StagePermission) | - |
| 14 | `/request-actions/{id}/delete-input-file/` | DELETE | delete_input_file | حذف ملف المدخل | INPUT (StagePermission) | - |
| 15 | `/request-actions/{id}/delete-output-file/` | DELETE | delete_output_file | حذف ملف المخرج | OUTPUT (StagePermission) | - |
| 16 | `/request-actions/{id}/add-note/` | POST | add_note | إضافة ملاحظة للمرحلة | NOTE (StagePermission) | - |
| 17 | `/request-actions/my-pending-stages/` | GET | my_pending_stages | المراحل المعلقة للمستخدم الحالي | StagePermission | - |

---

## 4. GrantSource (مصادر المنح)

### Section Overview
| Field | Value |
|-------|-------|
| **اسم القسم بالعربي** | مصادر المنح |
| **Model** | `GrantSource` |
| **MVS** | `GrantSourceMVS` |
| **Base URL** | `/api/d-services/grant-sources/` |
| **Priority** | 🟡 Medium |
| **Status Field** | - |
| **Statuses** | - |
| **Permissions** | AllMVS defaults + BranchViewSetMixin |

### GrantSourceMVS APIs

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 1 | `/grant-sources/` | GET | list | قائمة مصادر المنح | - | - |
| 2 | `/grant-sources/{id}/` | GET | retrieve | تفاصيل مصدر منحة | - | - |
| 3 | `/grant-sources/` | POST | create | إنشاء مصدر منحة | - | - |
| 4 | `/grant-sources/{id}/` | PUT | update | تعديل مصدر منحة | - | - |
| 5 | `/grant-sources/{id}/` | DELETE | destroy | حذف مصدر منحة | - | - |

---

## 5. Permissions (الصلاحيات)

### Section Overview
| Field | Value |
|-------|-------|
| **اسم القسم بالعربي** | الصلاحيات |
| **Model** | `GroupServicePermission`, `StagePermission`, `ServiceWorkFlowStepPermission` |
| **MVS** | `GroupServicePermissionMVS`, `StagePermissionMVS` |
| **Base URL** | `/api/d-services/group-service-permissions/`, `/api/d-services/stage-permissions/` |
| **Priority** | 🟠 High |
| **Status Field** | - |
| **Statuses** | - |
| **Permissions** | `is_manager` |

### GroupServicePermissionMVS APIs

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 1 | `/group-service-permissions/` | GET | list | قائمة صلاحيات المجموعات لخدمة (Query: `fk_service`) | is_manager | - |
| 2 | `/group-service-permissions/` | POST | create | إنشاء/تحديث صلاحيات المجموعات | is_manager | - |

**Request Body (create):**
```json
{
    "fk_service": 1,
    "groups": [
        {"fk_group": 1, "permissions": ["CREATE", "READ", "UPDATE"]},
        {"fk_group": 2, "permissions": ["CREATE", "DELETE", "PRINT"]}
    ]
}
```

### StagePermissionMVS APIs

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 3 | `/stage-permissions/` | GET | list | قائمة صلاحيات المستخدمين لخطوة (Query: `fk_workflow_step`) | is_manager | - |
| 4 | `/stage-permissions/` | POST | create | إنشاء/تحديث صلاحيات المستخدمين | is_manager | - |

**Request Body (create):**
```json
{
    "fk_workflow_step": 1,
    "users": [
        {"fk_user": 1, "permissions": ["START", "APPROVE"]},
        {"fk_user": 2, "permissions": ["EXECUTE"]}
    ]
}
```

**Response (list/create):**
```json
{
    "fk_workflow_step": 1,
    "workflow_step_name": "...",
    "users": [
        {"fk_user": 1, "username": "...", "full_name": "...", "permissions": ["START", "APPROVE"]}
    ]
}
```

---

## 6. ServiceLogs (سجلات الخدمات - متقدم)

### Section Overview
| Field | Value |
|-------|-------|
| **اسم القسم بالعربي** | سجلات الخدمات المتقدمة |
| **Model** | `ServiceLog` |
| **MVS** | `ServiceLogsViewSet` |
| **Base URL** | `/api/d-services/service-logs/` |
| **Priority** | 🟢 Normal |
| **Status Field** | `severity` |
| **Statuses** | `INFO`, `WARNING`, `ERROR`, `CRITICAL`, `DEBUG` |
| **Permissions** | IsAuthenticated |

### ServiceLogsViewSet APIs

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 1 | `/service-logs/` | GET | list | قائمة السجلات مع فلاتر متقدمة | - | - |
| 2 | `/service-logs/{id}/` | GET | retrieve | تفاصيل سجل معين | - | - |
| 3 | `/service-logs/by-service/` | GET | by_service | سجلات خدمة معينة (Query: `service_id`, `limit`) | - | - |
| 4 | `/service-logs/timeline/` | GET | timeline | عرض timeline للخدمة (Query: `service_id`) | - | - |
| 5 | `/service-logs/statistics/` | GET | statistics | إحصائيات السجلات (Query: `service_id`, `days`) | - | - |
| 6 | `/service-logs/{id}/add-note/` | POST | add_note | إضافة ملاحظة للسجل | - | - |
| 7 | `/service-logs/{id}/flag/` | POST | flag | تعليم السجل للانتباه | - | `is_flagged: false → true` |
| 8 | `/service-logs/{id}/unflag/` | POST | unflag | إزالة تعليم السجل | - | `is_flagged: true → false` |
| 9 | `/service-logs/{id}/mark-reviewed/` | POST | mark_reviewed | تعليم السجل كمراجع | - | `is_reviewed: false → true` |
| 10 | `/service-logs/alerts/` | GET | alerts | التنبيهات النشطة (المعلمة غير المراجعة) | - | - |
| 11 | `/service-logs/flagged/` | GET | flagged | جميع السجلات المعلمة | - | - |
| 12 | `/service-logs/critical/` | GET | critical | السجلات الحرجة (ERROR, CRITICAL) | - | - |
| 13 | `/service-logs/export/` | GET | export | تصدير السجلات (Query: `service_id`, `days`, `format`) | - | - |

---

## 7. RequestLogs (سجلات الطلبات - متقدم)

### Section Overview
| Field | Value |
|-------|-------|
| **اسم القسم بالعربي** | سجلات الطلبات المتقدمة |
| **Model** | `RequestLog`, `WorkflowLog` |
| **MVS** | `RequestLogsViewSet`, `WorkflowLogsViewSet` |
| **Base URL** | `/api/d-services/request-logs/`, `/api/d-services/workflow-logs/` |
| **Priority** | 🟢 Normal |
| **Status Field** | `severity`, `sla_status` |
| **Statuses** | `INFO`, `WARNING`, `ERROR`, `CRITICAL` / `ON_TIME`, `WARNING`, `BREACHED` |
| **Permissions** | IsAuthenticated + BranchViewSetMixin |

### RequestLogsViewSet APIs

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 1 | `/request-logs/` | GET | list | قائمة سجلات الطلبات | - | - |
| 2 | `/request-logs/by-request/` | GET | by_request | سجلات طلب معين (Query: `request_id`, `limit`) | - | - |
| 3 | `/request-logs/timeline/` | GET | timeline | timeline للطلب (Query: `request_id`) | - | - |
| 4 | `/request-logs/status-changes/` | GET | status_changes | تغييرات الحالة (Query: `request_id`) | - | - |
| 5 | `/request-logs/statistics/` | GET | statistics | إحصائيات السجلات | - | - |
| 6 | `/request-logs/{id}/add-note/` | POST | add_note | إضافة ملاحظة للسجل | - | - |
| 7 | `/request-logs/{id}/flag/` | POST | flag | تعليم السجل | - | - |
| 8 | `/request-logs/alerts/` | GET | alerts | التنبيهات النشطة | - | - |

### WorkflowLogsViewSet APIs

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 9 | `/workflow-logs/` | GET | list | قائمة سجلات سير العمل | - | - |
| 10 | `/workflow-logs/by-request/` | GET | by_request | سجلات طلب معين | - | - |
| 11 | `/workflow-logs/transitions/` | GET | transitions | الانتقالات بين المراحل (Query: `request_id`) | - | - |
| 12 | `/workflow-logs/sla-report/` | GET | sla_report | تقرير SLA (Query: `days`, `service_id`) | - | - |
| 13 | `/workflow-logs/overdue/` | GET | overdue | المراحل المتأخرة | - | - |
| 14 | `/workflow-logs/performance/` | GET | performance | تقرير الأداء (Query: `request_id`) | - | - |
| 15 | `/workflow-logs/stage-stats/` | GET | stage_stats | إحصائيات حسب المرحلة (Query: `stage_id`) | - | - |
| 16 | `/workflow-logs/{id}/add-note/` | POST | add_note | إضافة ملاحظة | - | - |
| 17 | `/workflow-logs/{id}/flag/` | POST | flag | تعليم السجل | - | - |

---

## 8. Logs (السجلات الأساسية)

### Section Overview
| Field | Value |
|-------|-------|
| **اسم القسم بالعربي** | السجلات الأساسية |
| **Model** | `ServiceLog`, `RequestLog`, `WorkflowLog`, `RequestReturnLog` |
| **MVS** | `ServiceLogViewSet`, `RequestLogViewSet`, `WorkflowLogViewSet`, `RequestReturnLogViewSet` |
| **Base URL** | (غير مسجلة في urls.py - للاستخدام الداخلي) |
| **Priority** | 🔵 Low |
| **Status Field** | - |
| **Statuses** | - |
| **Permissions** | IsAuthenticated |

### Basic Log ViewSets (ReadOnly)

| # | ViewSet | Filter Fields | Description |
|---|---------|---------------|-------------|
| 1 | `ServiceLogViewSet` | `fk_service`, `action`, `fk_user` | سجلات الخدمات الأساسية |
| 2 | `RequestLogViewSet` | `fk_request`, `action`, `fk_user` | سجلات الطلبات الأساسية |
| 3 | `WorkflowLogViewSet` | `fk_request`, `fk_user` | سجلات سير العمل الأساسية |
| 4 | `RequestReturnLogViewSet` | `fk_request`, `return_reason`, `fk_returned_by`, `is_resolved` | سجلات الإرجاع |

---

## 9. Verifications (التحققات)

### Section Overview
| Field | Value |
|-------|-------|
| **اسم القسم بالعربي** | التحققات والشروط المسبقة |
| **Model** | `AudienceConditionVerification` |
| **MVS** | `PrerequisiteVerificationViewSet` |
| **Base URL** | (Nested under requests) |
| **Priority** | 🟡 Medium |
| **Status Field** | `is_satisfied` |
| **Statuses** | `true`, `false` |
| **Permissions** | IsAuthenticated |

### PrerequisiteVerificationViewSet APIs

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 1 | `/.../{request_pk}/verifications/` | GET | list | قائمة التحققات للطلب | - | - |
| 2 | `/.../{request_pk}/verifications/verify/` | POST | verify_prerequisites | تنفيذ جميع التحققات للطلب | - | - |

---

## 10. Components (المكونات)

### Section Overview
| Field | Value |
|-------|-------|
| **اسم القسم بالعربي** | مكونات الخدمة والـ Schema |
| **Model** | - |
| **MVS** | `ServiceSchemaAPIView` |
| **Base URL** | `/api/d-services/service-schema/` |
| **Priority** | 🟠 High |
| **Status Field** | - |
| **Statuses** | - |
| **Permissions** | IsAuthenticated + CREATE permission |

### ServiceSchemaAPIView APIs

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 1 | `/service-schema/{pk}/` | GET | get | جلب مخطط الخدمة للإنشاء | CREATE (ServicePermission) | - |

**Response:**
```json
{
    "fk_service": 1,
    "fk_service__name": "...",
    "fk_service__code": "...",
    "input_template_type": "...",
    "output_template_type": "...",
    "target_audience_component": "...",
    "target_audience_schema": {...},
    "base_audience_component": "...",
    "base_audience_schema": {...},
    "version_name": "...",
    "version_schema": {...},
    "component_type": "...",
    "next_request_number": "REQ-000001",
    "request_date": "2025-12-29"
}
```

---

## 11. ExternalMethods (الدوال الخارجية)

### Section Overview
| Field | Value |
|-------|-------|
| **اسم القسم بالعربي** | الدوال الخارجية |
| **Model** | - |
| **MVS** | `AvailableFunctionsView` |
| **Base URL** | `/api/d-services/available-functions/` |
| **Priority** | 🔵 Low |
| **Status Field** | - |
| **Statuses** | - |
| **Permissions** | IsAuthenticated |

### AvailableFunctionsView APIs

| # | Endpoint | Method | Name | Description | Permissions | Status Transition |
|---|----------|--------|------|-------------|-------------|-------------------|
| 1 | `/available-functions/` | GET | get | قائمة الدوال المتاحة مع تفاصيلها | IsAuthenticated | - |

**Response:**
```json
{
    "success": true,
    "message": "تم جلب قائمة الدوال بنجاح",
    "data": [
        {"name": "function_name", "docstring": "..."}
    ],
    "count": 5
}
```

---

## ملحق: الخيارات والحالات

### ServicePermissionType
| Value | Display |
|-------|---------|
| CREATE | إنشاء طلب |
| READ | عرض الطلبات |
| UPDATE | تعديل الطلب |
| DELETE | حذف الطلب |
| PRINT | طباعة الطلب |
| START | بدء الطلب |
| APPROVE | الموافقة |
| REJECT | الرفض |
| LOCK | قفل الطلب |
| UNLOCK | فتح الطلب |
| CANCEL | إلغاء الطلب |
| COMPLETE | إكمال الطلب |
| ASSIGN_GRANT | تخصيص منحة |
| APPROVE_GRANT | الموافقة على المنحة |
| UPDATE_GRANT | تحديث المنحة |
| CANCEL_GRANT | إلغاء المنحة |
| REJECT_GRANT | رفض المنحة |
| ADD_DISCOUNT | إضافة خصم |
| APPROVE_DISCOUNT | الموافقة على الخصم |
| UPDATE_DISCOUNT | تحديث الخصم |
| CANCEL_DISCOUNT | إلغاء الخصم |
| REJECT_DISCOUNT | رفض الخصم |
| GET_INPUT_DATA | جلب بيانات المدخل |
| GET_OUTPUT_DATA | جلب بيانات المخرج |
| UPLOAD_INPUT | رفع ملف المدخل |
| UPLOAD_OUTPUT | رفع ملف المخرج |
| DELETE_INPUT | حذف ملف المدخل |
| DELETE_OUTPUT | حذف ملف المخرج |

### ActionPermissionType
| Value | Display |
|-------|---------|
| START | بدء المرحلة |
| COMPLETE | إكمال المرحلة |
| APPROVE | الموافقة |
| REJECT | الرفض |
| RETURN | إرجاع |
| ADVANCE | الانتقال للتالي |
| EXECUTE | تنفيذ |
| INPUT | إدارة المدخلات |
| OUTPUT | إدارة المخرجات |
| NOTE | إضافة ملاحظة |

### ServiceRequestStatusChoice
| Value | Display |
|-------|---------|
| PENDING | قيد الانتظار |
| IN_PROGRESS | قيد المعالجة |
| COMPLETED | مكتمل |
| REJECTED | مرفوض |
| CANCELLED | ملغي |

### StageStatusChoice
| Value | Display |
|-------|---------|
| PENDING | قيد الانتظار |
| IN_PROGRESS | قيد المعالجة |
| COMPLETED | مكتمل |
| REJECTED | مرفوض |
| RETURNED | مرجع |
| SKIPPED | تم تخطيه |

### GrantStatusChoice / DiscountStatusChoice
| Value | Display |
|-------|---------|
| PENDING | قيد الانتظار |
| APPROVED | موافق عليه |
| REJECTED | مرفوض |
| CANCELLED | ملغي |

### LogSeverityChoice
| Value | Display |
|-------|---------|
| INFO | معلومات |
| WARNING | تحذير |
| ERROR | خطأ |
| CRITICAL | حرج |
| DEBUG | تصحيح |

### SLAStatusChoice
| Value | Display |
|-------|---------|
| ON_TIME | في الوقت |
| WARNING | تحذير |
| BREACHED | تجاوز |

---

> **ملاحظة:** جميع الـ APIs تتطلب `Authorization: Bearer <token>` في الـ Header
