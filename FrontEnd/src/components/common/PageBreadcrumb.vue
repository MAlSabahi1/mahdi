<template>
  <!-- Deprecated: Replaced by the universal AppBreadcrumbs in AdminLayout -->
</template>

<script setup lang="ts">
// Kept to prevent breaking imports in other files
interface BreadcrumbProps {
  pageTitle: string
}
defineProps<BreadcrumbProps>()
</script>
