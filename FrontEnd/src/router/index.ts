import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useSystemStore } from '@/stores/system'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { left: 0, top: 0 }
  },
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: () => import('../views/Ecommerce.vue'),
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
      component: () => import('../views/Pages/BlankPage.vue'),
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
      },
    },
    {
      path: '/secretariat/correspondences',
      name: 'SecretariatCorrespondences',
      component: () => import('@/views/Secretariat/CorrespondenceList.vue'),
      meta: {
        title: 'صادر ووارد',
        requiresAuth: true,
      },
    },
    {
      path: '/secretariat/tasks',
      name: 'SecretariatTasks',
      component: () => import('@/views/Secretariat/TasksBoard.vue'),
      meta: {
        title: 'إدارة المهام',
        requiresAuth: true,
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
      path: '/services/export-config',
      name: 'ExcelExportConfigurator',
      component: () => import('@/views/Services/ExcelExportConfigurator.vue'),
      meta: {
        title: 'إعداد وتصدير النماذج المقفلة',
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
      path: '/services/request',
      name: 'UnifiedRequestForm',
      component: () => import('@/views/Services/UnifiedRequestForm.vue'),
      meta: {
        title: 'واجهة تقديم الطلب الموحدة',
        requiresAuth: true,
      },
    },
    {
      path: '/services/inbox',
      name: 'InboxTransactions',
      component: () => import('@/views/Services/InboxTransactions.vue'),
      meta: {
        title: 'قائمة المعاملات والمهام',
        requiresAuth: true,
      },
    },
    {
      path: '/services/workflows',
      name: 'WorkflowTracking',
      component: () => import('@/views/Services/WorkflowTracking.vue'),
      meta: {
        title: 'تتبع سير الموافقات',
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
      path: '/blank',
      name: 'Blank',
      component: () => import('../views/Pages/BlankPage.vue'),
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
