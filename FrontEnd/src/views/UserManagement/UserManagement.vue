<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="$t('users.title')" />
    
    <div class="space-y-6">
      <!-- Toolbar Component (Search, Columns selection, Filter status, add new user) -->
      <UserToolbar
        v-model:searchQuery="searchQuery"
        v-model:filterActive="filterActive"
        v-model:showFiltersPanel="showFiltersPanel"
        :columns="columns"
        @refresh="loadUsers(usersStore.currentPage)"
        @filter-changed="loadUsers(1)"
        @add-new="showCreateModal = true"
      />

      <!-- Table Component -->
      <UsersTable
        v-model:selectedUserIds="selectedUserIds"
        v-model:selectAll="selectAll"
        :users="usersStore.users"
        :loading="usersStore.loading"
        :error="usersStore.error"
        :columns="columns"
        :isColumnVisible="isColumnVisible"
        :splitName="splitName"
        :currentPage="usersStore.currentPage"
        :pageSize="pageSize"
        @toggle-select-all="toggleSelectAll"
        @toggle-staff="handleToggleStaff"
        @reset-password="openResetPasswordModal"
        @deactivate="handleDeactivate"
        @activate="handleActivate"
        @edit="openEditModal"
        @delete="handleDeleteUser"
        @retry="loadUsers()"
      />

      <!-- Pagination Component -->
      <TablePagination
        v-if="!usersStore.loading && usersStore.users.length > 0"
        :currentPage="usersStore.currentPage"
        :totalPages="usersStore.totalPages"
        :totalCount="usersStore.totalCount"
        :pageSize="pageSize"
        :visiblePages="visiblePages"
        @change-page="goToPage"
        @change-page-size="pageSize = $event; loadUsers(1)"
      />
    </div>

    <!-- Modals -->
    <CreateUserModal
      v-if="showCreateModal"
      @close="showCreateModal = false"
      @created="onUserCreated"
    />
    <EditUserModal
      v-if="showEditModal && selectedUser"
      :user="selectedUser"
      @close="showEditModal = false"
      @updated="onUserUpdated"
    />
    <ResetPasswordModal
      v-if="showResetModal && selectedUser"
      :user="selectedUser"
      @close="showResetModal = false"
      @reset="onPasswordReset"
    />
  </admin-layout>
</template>

<script setup lang="ts">
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import TablePagination from '@/components/common/TablePagination.vue'
import UserToolbar from './components/UserToolbar.vue'
import UsersTable from './components/UsersTable.vue'
import CreateUserModal from './components/CreateUserModal.vue'
import EditUserModal from './components/EditUserModal.vue'
import ResetPasswordModal from './components/ResetPasswordModal.vue'
import { useUserManagement } from '@/composables/useUserManagement'

const {
  usersStore,
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
} = useUserManagement()
</script>
