import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useSystemStore } from '@/stores/system'

// Augment Vue Router's RouteMeta to include our custom fields
declare module 'vue-router' {
  interface RouteMeta {
    title?: string
    requiresAuth?: boolean
    requiresAdmin?: boolean
    requiresPermission?: string | string[]
    guest?: boolean
  }
}


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { left: 0, top: 0 }
  },
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: () => import('@/views/SystemAdmin/Dashboard/StatsDashboard.vue'),
      meta: {
        title: 'Dashboard',
        requiresAuth: true,
      },
    },
    {
      path: '/users',
      name: 'UserManagement',
      component: () => import('../views/UserManagement/UserManagement.vue'),
      meta: {
        title: 'إدارة المستخدمين',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/users/governance',
      name: 'AccountGovernance',
      component: () => import('@/views/UserManagement/AccountGovernanceDashboard.vue'),
      meta: {
        title: 'حوكمة الحسابات وأمن النظام',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/users/sessions',
      name: 'ActiveSessions',
      component: () => import('@/views/UserManagement/ActiveSessions.vue'),
      meta: {
        title: 'إدارة الجلسات والأجهزة النشطة',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/users/audit-trail',
      name: 'AuditTrail',
      component: () => import('@/views/UserManagement/AuditTrail.vue'),
      meta: {
        title: 'السجل المركزي لتدقيق البيانات',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/users/policy-simulator',
      name: 'PolicySimulator',
      component: () => import('@/views/UserManagement/PolicySimulator.vue'),
      meta: {
        title: 'أداة محاكاة واختبار الصلاحيات',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/users/policy-matrix',
      name: 'PolicyMatrix',
      component: () => import('@/views/UserManagement/PolicyMatrix.vue'),
      meta: {
        title: 'مصفوفة صلاحيات الحقول والسياسات',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/users/emergency-access',
      name: 'EmergencyAccess',
      component: () => import('@/views/UserManagement/EmergencyAccess.vue'),
      meta: {
        title: 'تفويض الصلاحيات والوصول الطارئ',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/users/dual-auth',
      name: 'DualAuthHub',
      component: () => import('@/views/UserManagement/DualAuthHub.vue'),
      meta: {
        title: 'مجمع الاعتماد الثنائي',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/users/:id',
      name: 'user-details',
      component: () => import('@/views/UserManagement/UserDetails.vue'),

      meta: {
        title: 'تفاصيل المستخدم',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/users/policy-simulator',
      name: 'policy-simulator',
      component: () => import('@/views/UserManagement/PolicySimulator.vue'),
      meta: {
        title: 'محاكي الصلاحيات',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/roles',
      name: 'roles-management',
      component: () => import('@/views/UserManagement/RolesManagement.vue'),
      meta: {
        title: 'إدارة المجموعات والصلاحيات',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/roles/permission-groups',
      name: 'permission-groups',
      component: () => import('@/views/UserManagement/PermissionGroups.vue'),
      meta: {
        title: 'مجموعات الصلاحيات',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/roles/permissions',
      name: 'permissions-list',
      component: () => import('@/views/UserManagement/Permissions.vue'),
      meta: {
        title: 'الصلاحيات المباشرة',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/roles/create',
      name: 'role-create',
      component: () => import('@/views/UserManagement/RoleEditor.vue'),
      meta: {
        title: 'إضافة مجموعة جديدة',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/roles/:id/edit',
      name: 'role-edit',
      component: () => import('@/views/UserManagement/RoleEditor.vue'),
      meta: {
        title: 'تعديل بيانات وصلاحيات المجموعة',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/users/settings',
      name: 'security-settings',
      component: () => import('../views/Errors/FourZeroFour.vue'),
      meta: {
        title: 'الإعدادات الأمنية للنظام',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/audit',
      name: 'AuditLogs',
      component: () => import('@/views/Audit/AuditLogs.vue'),
      meta: {
        title: 'سجل التدقيق',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/admin/dashboard/stats',
      name: 'StatsDashboard',
      component: () => import('@/views/SystemAdmin/Dashboard/StatsDashboard.vue'),
      meta: {
        title: 'المؤشرات الإحصائية العامة',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/admin/dashboard/analytics',
      name: 'AnalyticsDashboard',
      component: () => import('@/views/SystemAdmin/Dashboard/AnalyticsDashboard.vue'),
      meta: {
        title: 'الداشبورد التحليلي الموحد',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/admin/dashboard/alerts',
      name: 'AlertsCenter',
      component: () => import('@/views/SystemAdmin/Dashboard/AlertsCenter.vue'),
      meta: {
        title: 'مركز التنبيهات والطلبات',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/admin/dashboard/compliance',
      name: 'ComplianceTracker',
      component: () => import('@/views/SystemAdmin/Dashboard/ComplianceTracker.vue'),
      meta: {
        title: 'متابعة التزام المحافظات',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/admin/structure/regions',
      name: 'RegionsConfig',
      component: () => import('@/views/SystemAdmin/Structure/RegionsConfig.vue'),
      meta: {
        title: 'تهيئة المحافظات والمديريات',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/admin/structure/geo-tree',
      name: 'GeoHierarchyTree',
      component: () => import('@/views/SystemAdmin/Structure/GeoHierarchyTree.vue'),
      meta: {
        title: 'شجرة الهيكل الجغرافي',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: "/reports",
      redirect: "/reports/dashboard",
    },
    {
      path: "/reports/dashboard",
      name: "CentralReportsDashboard",
      component: () => import("@/views/Reports/ReportsDashboard.vue"),
      meta: {
        title: "وحدة التقارير والإحصائيات المركزية",
        requiresAuth: true
      }
    },
    {
      path: "/reports/graphical",
      name: "GraphicalReports",
      component: () => import("@/views/Reports/GraphicalReports.vue"),
      meta: {
        title: "التقارير الرسومية",
        requiresAuth: true
      }
    },
    {
      path: "/reports/view/1",
      name: "WorkforceSummaryReport",
      component: () => import("@/views/Reports/WorkforceSummaryReport.vue"),
      meta: {
        title: "خلاصة القوة العاملة",
        requiresAuth: true
      }
    },
    {
      path: "/reports/hierarchical",
      name: "HierarchicalReport",
      component: () => import("@/views/Reports/HierarchicalReport.vue"),
      meta: {
        title: "الهيكل التنظيمي والقوة الفعلية",
        requiresAuth: true
      }
    },
    {
      path: "/reports/view/2",
      name: "WorkforceCategoricalReport",
      component: () => import("@/views/Reports/WorkforceCategoricalReport.vue"),
      meta: {
        title: "خلاصة فئوية للقوة العاملة",
        requiresAuth: true
      }
    },
    {
      path: "/reports/view/3",
      name: "NonWorkforceReport",
      component: () => import("@/views/Reports/NonWorkforceReport.vue"),
      meta: {
        title: "خلاصة القوة غير العاملة",
        requiresAuth: true
      }
    },
    {
      path: "/reports/export-requests",
      name: "ExportRequestsManagement",
      component: () => import("@/views/Reports/ExportRequestsManagement.vue"),
      meta: {
        title: "إدارة طلبات التصدير",
        requiresAuth: true,
        permissions: ["secretariat.task.execute"] // Using an existing permission for demo
      }
    },
    {
      path: "/reports/view/4",
      name: "ActiveForceReport",
      component: () => import("@/views/Reports/ActiveForceReport.vue"),
      meta: {
        title: "كشف القوة العاملة فعلياً",
        requiresAuth: true
      }
    },
    {
      path: "/reports/view/:id(4b1|4b2)",
      name: "InactiveActualForceReport",
      component: () => import("@/views/Reports/InactiveActualForceReport.vue"),
      meta: {
        title: "القوة العاملة الغير فعلية",
        requiresAuth: true
      }
    },
    {
      path: "/reports/builder/studio/:id?",
      name: "ReportStudio",
      component: () => import("@/views/Reports/Builder/ReportStudio.vue"),
      meta: {
        title: "تصميم تقرير مخصص",
        requiresAuth: true,
        requiresAdmin: true
      }
    },
    {
      path: "/reports/builder/view/:id",
      name: "CustomReportViewer",
      component: () => import("@/views/Reports/Builder/CustomReportViewer.vue"),
      meta: {
        title: "عرض تقرير مخصص",
        requiresAuth: true
      }
    },
    {
      path: "/reports/view/:id(5|6|7|8|9|10|11)",
      name: "UnifiedListReport",
      component: () => import("@/views/Reports/UnifiedListReport.vue"),
      meta: {
        title: "كشوفات القوة غير العاملة مؤقتاً",
        requiresAuth: true
      }
    },
    {
      path: "/reports/view/12",
      name: "OldAgeReport",
      component: () => import("@/views/Reports/OldAgeReport.vue"),
      meta: { title: "كشف كبار سن", requiresAuth: true }
    },
    {
      path: "/reports/view/13",
      name: "EndOfServiceReport",
      component: () => import("@/views/Reports/EndOfServiceReport.vue"),
      meta: { title: "كشف نهاية المدة", requiresAuth: true }
    },
    {
      path: "/reports/view/14",
      name: "RetirementCandidatesReport",
      component: () => import("@/views/Reports/RetirementCandidatesReport.vue"),
      meta: { title: "كشف مرشحين للتقاعد", requiresAuth: true }
    },
    {
      path: "/reports/view/15",
      name: "MedicalUnfitnessReport",
      component: () => import("@/views/Reports/MedicalUnfitnessReport.vue"),
      meta: { title: "كشف عدم اللياقة", requiresAuth: true }
    },
    {
      path: "/reports/view/16",
      name: "MartyrsDeceasedReport",
      component: () => import("@/views/Reports/MartyrsDeceasedReport.vue"),
      meta: {
        title: "كشف شهداء ووفيات",
        requiresAuth: true
      }
    },
    {
      path: "/reports/view/17",
      name: "RetiredReport",
      component: () => import("@/views/Reports/RetiredReport.vue"),
      meta: { title: "كشف متقاعدين", requiresAuth: true }
    },
    {
      path: "/reports/view/18",
      name: "MinistryArrivalsReport",
      component: () => import("@/views/Reports/MinistryArrivalsReport.vue"),
      meta: { title: "كشف الواصلين من الوزارة", requiresAuth: true }
    },
    {
      path: "/reports/view/:id(19|20|21|22|23|24a|24b|25)",
      name: "AuditMovementReports",
      component: () => import("@/views/Reports/AuditMovementReports.vue"),
      meta: {
        title: "كشوفات التدقيق وحركة القوة",
        requiresAuth: true
      }
    },
    // Placeholder routes for Secretariat Reports
    {
      path: "/reports/secretariat/correspondences",
      name: "SecretariatCorrespondencesReport",
      component: () => import("../views/Errors/FourZeroFour.vue"),
      meta: { title: "تقرير المراسلات الواردة والصادرة", requiresAuth: true }
    },
    {
      path: "/reports/secretariat/tasks",
      name: "SecretariatTasksReport",
      component: () => import("../views/Errors/FourZeroFour.vue"),
      meta: { title: "تقرير إنجاز المهام", requiresAuth: true }
    },
    {
      path: "/reports/secretariat/meetings",
      name: "SecretariatMeetingsReport",
      component: () => import("../views/Errors/FourZeroFour.vue"),
      meta: { title: "تقرير الاجتماعات", requiresAuth: true }
    },
    // Placeholder routes for Administration Reports
    {
      path: "/reports/admin/stats",
      name: "AdminStatsReport",
      component: () => import("../views/Errors/FourZeroFour.vue"),
      meta: { title: "الإحصائيات العامة للنظام", requiresAuth: true }
    },
    {
      path: "/reports/admin/users-activity",
      name: "AdminUsersActivityReport",
      component: () => import("../views/Errors/FourZeroFour.vue"),
      meta: { title: "تقرير نشاط المستخدمين", requiresAuth: true }
    },
    {
      path: "/reports/admin/audit",
      name: "AdminAuditReport",
      component: () => import("../views/Errors/FourZeroFour.vue"),
      meta: { title: "سجل التدقيق والمراجعة", requiresAuth: true }
    },
    {
      path: '/admin/snapshots',
      name: 'MonthlySnapshots',
      component: () => import('@/views/SystemAdmin/MonthlySnapshots.vue'),
      meta: {
        title: 'الأرشيف واللقطة الشهرية',
        requiresAuth: true
      }
    },
    {
      path: '/admin/documents/list',
      name: 'DocumentFormsList',
      component: () => import('@/views/SystemAdmin/DocumentBuilder/DocumentFormsList.vue'),
      meta: {
        title: 'قائمة الاستمارات الديناميكية',
        requiresAuth: true,
        requiresAdmin: true
      }
    },
    {
      path: '/admin/documents/builder/:id?',
      name: 'DocumentFormBuilder',
      component: () => import('@/views/SystemAdmin/DocumentBuilder/DocumentFormBuilder.vue'),
      meta: {
        title: 'مصمم الاستمارات',
        requiresAuth: true,
        requiresAdmin: true
      }
    },
    {
      path: '/admin/documents/preview/:id',
      name: 'DocumentFormPreview',
      component: () => import('@/views/SystemAdmin/DocumentBuilder/DocumentFormPreview.vue'),
      meta: {
        title: 'معاينة الاستمارة',
        requiresAuth: true,
        requiresAdmin: true
      }
    },
    {
      path: '/admin/documents/memo-builder',
      name: 'OfficialMemoBuilder',
      component: () => import('@/views/SystemAdmin/DocumentBuilder/OfficialMemoBuilder.vue'),
      meta: {
        title: 'منشئ المذكرات (Cover Memos)',
        requiresAuth: true,
        requiresAdmin: true
      }
    },
    {
      path: '/admin/documents/memo-preview',
      name: 'OfficialMemoPreview',
      component: () => import('@/views/SystemAdmin/DocumentBuilder/OfficialMemoPreview.vue'),
      meta: {
        title: 'معاينة المذكرة الرسمية',
        requiresAuth: true,
        requiresAdmin: true
      }
    },
    {
      path: '/admin/structure/org-tree',
      name: 'OrgHierarchyTree',
      component: () => import('@/views/SystemAdmin/Structure/OrgHierarchyTree.vue'),
      meta: {
        title: 'شجرة الهيكل التنظيمي',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/admin/structure/general-configs',
      name: 'GeneralConfigs',
      component: () => import('@/views/SystemAdmin/Structure/GeneralConfigs.vue'),
      meta: {
        title: 'التهيئة العامة للهيكل',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/admin/system/seeding',
      name: 'InitialSeeding',
      component: () => import('@/views/SystemAdmin/System/InitialSeeding.vue'),
      meta: {
        title: 'معالج التأسيس الأولي',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/admin/system/telemetry',
      name: 'SystemTelemetry',
      component: () => import('@/views/SystemAdmin/System/SystemTelemetry.vue'),
      meta: {
        title: 'تليمتري النظام والمهام',
        requiresAuth: true,
        requiresAdmin: true,
      },
    },
    {
      path: '/personnel',
      name: 'PersonnelList',
      component: () => import('@/views/Personnel/PersonnelList.vue'),
      meta: {
        title: 'شؤون الأفراد',
        requiresAuth: true,
      },
    },
    {
      path: '/personnel/corrections',
      name: 'CorrectionsManagement',
      component: () => import('@/views/Personnel/CorrectionsManagement.vue'),
      meta: {
        title: 'إدارة طلبات التصحيح',
        requiresAuth: true,
      },
    },
    {
      path: '/personnel/settlements',
      name: 'RankSettlementsManagement',
      component: () => import('@/views/Personnel/RankSettlementsManagement.vue'),
      meta: {
        title: 'إدارة تسويات الرتب',
        requiresAuth: true,
      },
    },
    {
      path: '/personnel/profile-search',
      name: 'PersonnelProfileSearch',
      component: () => import('@/views/Personnel/PersonnelProfileSearch.vue'),
      meta: {
        title: 'الملف الكامل للمنتسب',
        requiresAuth: true,
      },
    },
    {
      path: '/personnel/create',
      name: 'PersonnelCreate',
      component: () => import('@/views/Personnel/PersonnelCreate.vue'),
      meta: {
        title: 'إضافة فرد جديد',
        requiresAuth: true,
      },
    },
    {
      path: '/personnel/:id',
      name: 'PersonnelDetail',
      component: () => import('@/views/Personnel/PersonnelDetail.vue'),
      meta: {
        title: 'الملف الشخصي',
        requiresAuth: true,
      },
    },
    {
      path: '/personnel/:id/edit',
      name: 'PersonnelEdit',
      component: () => import('@/views/Personnel/PersonnelEdit.vue'),
      meta: {
        title: 'تعديل بيانات الفرد',
        requiresAuth: true,
      },
    },
    {
      path: '/services/dashboard',
      name: 'ServiceCycleDashboard',
      component: () => import('@/views/Services/ServiceCycleDashboard.vue'),
      meta: {
        title: 'لوحة التحكم الكشوفات',
        requiresAuth: true,
      },
    },
    {
      path: '/secretariat/dashboard',
      name: 'SecretariatDashboard',
      component: () => import('@/views/Secretariat/Dashboard.vue'),
      meta: {
        title: 'لوحة تحكم السكرتارية',
        requiresAuth: true,
        requiresPermission: 'secretariat.view.all',
      },
    },
    {
      path: '/secretariat/correspondences',
      name: 'SecretariatCorrespondences',
      component: () => import('@/views/Secretariat/CorrespondenceList.vue'),
      meta: {
        title: 'صادر ووارد',
        requiresAuth: true,
        requiresPermission: ['secretariat.view.all', 'secretariat.view.own'],
      },
    },
    {
      path: '/secretariat/correspondences/:id',
      name: 'SecretariatCorrespondenceDetail',
      component: () => import('@/views/Secretariat/CorrespondenceDetail.vue'),
      meta: {
        title: 'تفاصيل وأرشفة المراسلة',
        requiresAuth: true,
        requiresPermission: ['secretariat.view.all', 'secretariat.view.own', 'secretariat.task.execute'],
      },
    },
    {
      path: '/secretariat/tasks',
      name: 'SecretariatTasks',
      component: () => import('@/views/Secretariat/TasksBoard.vue'),
      meta: {
        title: 'إدارة المهام',
        requiresAuth: true,
        requiresPermission: ['secretariat.task.manage', 'secretariat.task.execute'],
      },
    },
    {
      path: '/secretariat/meetings',
      name: 'SecretariatMeetings',
      component: () => import('@/views/Secretariat/MeetingMinutes.vue'),
      meta: {
        title: 'محاضر الاجتماعات',
        requiresAuth: true,
        requiresPermission: 'secretariat.view.all',
      },
    },
    {
      path: '/secretariat/inventory',
      name: 'SecretariatInventory',
      component: () => import('@/views/Secretariat/InventoryCustody.vue'),
      meta: {
        title: 'القرطاسية والعهد والمخزن',
        requiresAuth: true,
        requiresPermission: 'secretariat.view.all',
      },
    },
    {
      path: '/secretariat/attendance',
      name: 'SecretariatAttendance',
      component: () => import('@/views/Secretariat/AttendanceMonitoring.vue'),
      meta: {
        title: 'رقابة الحضور والدوام',
        requiresAuth: true,
        requiresPermission: 'secretariat.view.all',
      },
    },
    {
      path: '/secretariat/finance',
      name: 'SecretariatFinance',
      component: () => import('@/views/Secretariat/FinancialAllocations.vue'),
      meta: {
        title: 'الاعتماد المالي والمصروفات',
        requiresAuth: true,
        requiresPermission: 'secretariat.view.all',
      },
    },
    {
      path: '/secretariat/document-requests',
      name: 'SecretariatDocumentRequests',
      component: () => import('@/views/Secretariat/DocumentRequests.vue'),
      meta: {
        title: 'طلبات الأعمال المكتبية وصياغة الخطابات',
        requiresAuth: true,
        requiresPermission: 'secretariat.view.all',
      },
    },
    {
      path: '/services/staging',
      name: 'StagingList',
      component: () => import('@/views/Services/StagingList.vue'),
      meta: {
        title: 'مراجعة الاعتمادات',
        requiresAuth: true,
      },
    },
    {
      path: '/services/rejections',
      name: 'RejectionList',
      component: () => import('@/views/Services/RejectionList.vue'),
      meta: {
        title: 'سجل المرفوضات',
        requiresAuth: true,
      },
    },
    {
      path: '/services/reconciliation',
      name: 'ReconciliationList',
      component: () => import('@/views/Services/ReconciliationList.vue'),
      meta: {
        title: 'المطابقات',
        requiresAuth: true,
      },
    },
    {
      path: '/services/reconciliation/:id',
      name: 'ReconciliationDetail',
      component: () => import('@/views/Services/ReconciliationDetail.vue'),
      meta: {
        title: 'تفاصيل المطابقة',
        requiresAuth: true,
      },
    },
    {
      path: '/services/reports',
      name: 'ReportsDashboard',
      component: () => import('@/views/Services/ReportsDashboard.vue'),
      meta: {
        title: 'التقارير والإقفال',
        requiresAuth: true,
      },
    },
    {
      path: '/services/import-wizard',
      name: 'ExcelImportWizard',
      component: () => import('@/views/Services/ExcelImportWizard.vue'),
      meta: {
        title: 'معالج الاستيراد الجماعي وتتبع Celery',
        requiresAuth: true,
      },
    },
    {
      path: '/services/export-config',
      name: 'ExcelExportConfigurator',
      component: () => import('@/views/Services/ExcelExportConfigurator.vue'),
      meta: {
        title: 'إعداد وتصدير النماذج المقفلة',
        requiresAuth: true,
      },
    },
    {
      path: '/services/monthly-exports',
      name: 'MonthlyExports',
      component: () => import('@/views/Services/MonthlyExports.vue'),
      meta: {
        title: 'تصدير التقارير الشهرية الموحدة',
        requiresAuth: true,
      },
    },
    {
      path: '/services/official-reports',
      name: 'OfficialReports',
      component: () => import('@/views/Services/OfficialReports.vue'),
      meta: {
        title: 'تصدير التقارير الرسمية',
        requiresAuth: true,
      },
    },
    {
      path: '/services/directory',
      name: 'ServiceDirectory',
      component: () => import('@/views/Services/ServiceDirectory.vue'),
      meta: {
        title: 'دليل الخدمات والاستمارات',
        requiresAuth: true,
      },
    },
    {
      path: '/services/builder',
      name: 'ServiceBuilder',
      component: () => import('@/views/Services/ServiceBuilder.vue'),
      meta: {
        title: 'مُنشئ الخدمات (Admin)',
        requiresAuth: true,
      },
    },
    {
      path: '/services/workflow-builder',
      name: 'WorkflowBuilder',
      component: () => import('@/views/Services/WorkflowBuilder.vue'),
      meta: {
        title: 'مُنشئ مسارات العمل (Admin)',
        requiresAuth: true,
      },
    },
    {
      path: '/services/request',
      name: 'UnifiedRequestForm',
      component: () => import('@/views/Services/UnifiedRequestForm.vue'),
      meta: {
        title: 'واجهة تقديم الطلب الموحدة',
        requiresAuth: true,
      },
    },
    {
      path: '/services/request/correction',
      name: 'CorrectionRequestForm',
      component: () => import('@/views/Services/Specialized/CorrectionRequestForm.vue'),
      meta: {
        title: 'طلب تصحيح بيانات',
        requiresAuth: true,
      },
    },
    {
      path: '/services/request/rank-settlement',
      name: 'RankSettlementRequestForm',
      component: () => import('@/views/Services/Specialized/RankSettlementRequestForm.vue'),
      meta: {
        title: 'تسوية وترقية الرتب',
        requiresAuth: true,
      },
    },
    // ── مركز المعاملات الموحد ──
    {
      path: '/services/transactions',
      name: 'TransactionsHub',
      component: () => import('@/views/Services/TransactionsHub.vue'),
      meta: {
        title: 'مركز المعاملات والمتابعة',
        requiresAuth: true,
      },
    },
    // ── Redirects من المسارات القديمة ──
    { path: '/services/inbox', redirect: '/services/transactions?tab=all' },
    { path: '/services/requests', redirect: '/services/transactions?tab=all' },
    { path: '/services/external-requests', redirect: '/services/transactions?tab=external' },
    { path: '/services/internal-requests', redirect: '/services/transactions?tab=internal' },
    { path: '/services/workflows', redirect: '/services/transactions?tab=tracking' },
    {
      path: '/services/forms/:id',
      name: 'FormDetail',
      component: () => import('@/views/Services/FormDetail.vue'),
      meta: {
        title: 'تفاصيل المعاملة',
        requiresAuth: true,
      },
    },
    {
      path: '/services/editor-react',
      name: 'ServicesEditorReact',
      component: () => import('@/views/Services/VueGridEditor.vue'),
      meta: {
        title: 'تعديل الخدمات المطور (React)',
        requiresAuth: true,
      },
    },
    {
      path: '/services/print/model-23/:id',
      name: 'model-23-print',
      component: () => import('@/views/Services/PrintTemplates/Model23PrintView.vue'),
      meta: {
        title: 'طباعة نموذج 23',
        requiresAuth: true,
      },
    },
    {
      path: '/blank',
      name: 'Blank',
      component: () => import('../views/Errors/FourZeroFour.vue'),
      meta: {
        title: 'Blank',
        requiresAuth: true,
      },
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('../views/Others/UserProfile.vue'),
      meta: {
        title: 'الملف الشخصي',
        requiresAuth: true,
      },
    },
    {
      path: '/error-404',
      name: '404 Error',
      component: () => import('../views/Errors/FourZeroFour.vue'),
      meta: {
        title: '404 Error',
      },
    },
    {
      path: '/signin',
      name: 'Signin',
      component: () => import('../views/Auth/Signin.vue'),
      meta: {
        title: 'تسجيل الدخول',
        guest: true,
      },
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/error-404',
    },
  ],
})

export default router

function getSystemFromPath(path: string, currentSystem: string): string {
  if (path === '/') {
    return currentSystem
  }
  if (path.startsWith('/secretariat')) {
    return 'secretariat'
  }
  if (path.startsWith('/personnel') || path.startsWith('/services')) {
    return 'services_personnel'
  }
  if (path.startsWith('/users') || path.startsWith('/roles')) {
    return 'users_permissions'
  }
  if (path.startsWith('/admin') || path.startsWith('/audit')) {
    return 'administration'
  }
  if (path.startsWith('/reports')) {
    return 'reports'
  }
  return currentSystem
}

router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title ? to.meta.title + ' | ' : ''}Admin Dashboard`

  const authStore = useAuthStore()
  const systemStore = useSystemStore()

  // مزامنة حالة النظام النشط مع المسار الحالي
  const targetSystemId = getSystemFromPath(to.path, systemStore.currentSystem)
  if (systemStore.currentSystem !== targetSystemId) {
    systemStore.switchSystem(targetSystemId)
  }

  // إذا كانت الصفحة تتطلب مصادقة والمستخدم غير مسجل
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: 'Signin', query: { redirect: to.fullPath } })
  }

  // إذا كانت الصفحة تتطلب صلاحية مدير والمستخدم ليس مدير
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    return next({ name: 'Dashboard' })
  }

  // تحقق من الصلاحيات المحددة (ABAC)
  if (to.meta.requiresPermission && authStore.isAuthenticated) {
    const required = to.meta.requiresPermission
    // السوبر أدمين يمر دائماً
    if (!authStore.user?.is_superuser) {
      const hasAccess = Array.isArray(required)
        ? required.some((p: string) => authStore.hasPermission(p))
        : authStore.hasPermission(required as string)

      if (!hasAccess) {
        // إعادة توجيه لصفحة مهام الموظف إذا كان لديه صلاحية تنفيذ المهام
        if (authStore.hasPermission('secretariat.task.execute') && to.name !== 'SecretariatTasks') {
          return next({ name: 'SecretariatTasks' })
        }
        // وإلا للوحة الرئيسية
        return next({ name: 'Dashboard' })
      }
    }
  }

  // إذا كان المستخدم مسجل ويحاول الوصول لصفحة الضيف (تسجيل الدخول)
  if (to.meta.guest && authStore.isAuthenticated) {
    return next({ name: 'Dashboard' })
  }

  next()
})

router.afterEach((to) => {
  const path = to.fullPath
  // تجنب حفظ المسارات غير الصالحة أو الخاصة بالمصادقة أو الأخطاء
  if (
    path.startsWith('/signin') ||
    path.startsWith('/error') ||
    path.startsWith('/blank') ||
    path.startsWith('/profile')
  ) {
    return
  }
  const systemStore = useSystemStore()
  const systemId = getSystemFromPath(to.path, systemStore.currentSystem)
  sessionStorage.setItem(`pol_last_path_${systemId}`, path)
})
