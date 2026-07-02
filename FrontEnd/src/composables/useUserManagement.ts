import { ref, watch, computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useUsersStore } from '@/stores/users'
import { useAuthStore } from '@/stores/auth'
import { useDebounce } from '@/composables/useDebounce'
import Swal from 'sweetalert2'

export function useUserManagement() {
  const usersStore = useUsersStore()
  const authStore = useAuthStore()

  // Bind all table & view state variables directly to Pinia central store
  const {
    searchQuery,
    filterActive,
    currentPage,
    pageSize,
    selectedUserIds,
    selectAll,
    columns
  } = storeToRefs(usersStore)

  const debouncedSearchQuery = useDebounce(searchQuery, 400)

  // Local UI-only state (e.g. dialog views/filters visibility)
  const showCreateModal = ref(false)
  const showEditModal = ref(false)
  const showResetModal = ref(false)
  const selectedUser = ref<any>(null)
  const showFiltersPanel = ref(false)

  const isColumnVisible = usersStore.isColumnVisible
  const toggleSelectAll = usersStore.toggleSelectAll

  function loadUsers(page = 1) {
    usersStore.fetchUsers(page)
  }

  watch(debouncedSearchQuery, () => {
    loadUsers(1)
  })

  function goToPage(page: number) {
    if (page >= 1 && page <= usersStore.totalPages) {
      loadUsers(page)
    }
  }

  function toggleFilters() {
    showFiltersPanel.value = !showFiltersPanel.value
  }

  function splitName(fullName: string) {
    if (!fullName) return { first: '—', last: '—' }
    const parts = fullName.trim().split(/\s+/)
    if (parts.length === 1) {
      return { first: parts[0], last: '—' }
    }
    const last = parts[parts.length - 1]
    const first = parts.slice(0, parts.length - 1).join(' ')
    return { first, last }
  }

  function showToast(message: string, type: 'success' | 'error' = 'success') {
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: type,
      title: message,
      showConfirmButton: false,
      timer: 3000
    })
  }

  async function handleToggleStaff(user: any) {
    if (user.id === authStore.user?.id) {
      Swal.fire({
        icon: 'error',
        title: 'تنبيه أمني',
        text: 'لا يمكنك إلغاء اعتماد حساب المسؤول الخاص بك لمنع انغلاق النظام عليك!',
        confirmButtonText: 'موافق'
      })
      return
    }

    try {
      await usersStore.updateUser(user.id, { is_staff: !user.is_staff })
      showToast(user.is_staff ? 'تم إلغاء الاعتماد كمدير' : 'تم اعتماد المستخدم كمدير بنجاح')
    } catch {
      showToast('فشل تعديل اعتماد المستخدم', 'error')
    }
  }

  async function handleDeleteUser(user: any) {
    if (user.id === authStore.user?.id) {
      Swal.fire({
        icon: 'error',
        title: 'تنبيه أمني',
        text: 'لا يمكنك حذف حساب المسؤول الحالي الذي تستخدمه لتسجيل الدخول!',
        confirmButtonText: 'موافق'
      })
      return
    }

    const result = await Swal.fire({
      title: 'حذف المستخدم',
      text: `هل أنت متأكد من حذف حساب "${user.display_name || user.username}" نهائياً؟`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#6B7280',
      confirmButtonText: 'نعم، احذف',
      cancelButtonText: 'إلغاء'
    })
    if (!result.isConfirmed) return
    try {
      await usersStore.deactivateUser(user.id)
      showToast('تم حذف المستخدم بنجاح')
    } catch {
      showToast('فشل حذف المستخدم', 'error')
    }
  }

  async function handleDeactivate(user: any) {
    if (user.id === authStore.user?.id) {
      Swal.fire({
        icon: 'error',
        title: 'تنبيه أمني',
        text: 'لا يمكنك تعطيل حساب المسؤول النشط الخاص بك!',
        confirmButtonText: 'موافق'
      })
      return
    }

    const result = await Swal.fire({
      title: 'تعطيل الحساب',
      text: `هل أنت متأكد من تعطيل حساب "${user.display_name || user.username}"؟`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#6B7280',
      confirmButtonText: 'نعم، تعطيل',
      cancelButtonText: 'إلغاء'
    })
    if (!result.isConfirmed) return
    try {
      await usersStore.deactivateUser(user.id)
      showToast('تم تعطيل الحساب بنجاح')
    } catch {
      showToast('فشل تعطيل الحساب', 'error')
    }
  }

  async function handleActivate(user: any) {
    try {
      await usersStore.activateUser(user.id)
      showToast('تم تفعيل الحساب بنجاح')
    } catch {
      showToast('فشل تفعيل الحساب', 'error')
    }
  }

  function openEditModal(user: any) {
    selectedUser.value = user
    showEditModal.value = true
  }

  function openResetPasswordModal(user: any) {
    selectedUser.value = user
    showResetModal.value = true
  }

  function onUserCreated() {
    showCreateModal.value = false
    showToast('تم إنشاء المستخدم بنجاح')
  }

  function onUserUpdated() {
    showEditModal.value = false
    showToast('تم تحديث المستخدم بنجاح')
  }

  function onPasswordReset() {
    showResetModal.value = false
    showToast('تم إعادة تعيين كلمة المرور بنجاح')
  }

  const visiblePages = computed(() => {
    const total = usersStore.totalPages
    const current = usersStore.currentPage
    const pages = []
    if (total <= 5) {
      for (let i = 1; i <= total; i++) pages.push(i)
    } else {
      if (current <= 3) {
        pages.push(1, 2, 3, 4, '...', total)
      } else if (current >= total - 2) {
        pages.push(1, '...', total - 3, total - 2, total - 1, total)
      } else {
        pages.push(1, '...', current - 1, current, current + 1, '...', total)
      }
    }
    return pages
  })

  onMounted(() => {
    usersStore.fetchRoles()
    loadUsers()
  })

  return {
    usersStore,
    authStore,
    searchQuery,
    filterActive,
    showCreateModal,
    showEditModal,
    showResetModal,
    selectedUser,
    showFiltersPanel,
    pageSize,
    selectedUserIds,
    selectAll,
    columns,
    isColumnVisible,
    loadUsers,
    goToPage,
    toggleFilters,
    toggleSelectAll,
    splitName,
    handleToggleStaff,
    handleDeleteUser,
    handleDeactivate,
    handleActivate,
    openEditModal,
    openResetPasswordModal,
    onUserCreated,
    onUserUpdated,
    onPasswordReset,
    visiblePages
  }
}
