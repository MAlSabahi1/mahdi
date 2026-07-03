import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

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

router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title ? to.meta.title + ' | ' : ''}Admin Dashboard`

  const authStore = useAuthStore()

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
