<template>
  <div class="administrative-empty-state pa-12 text-center">
    <!-- Static Professional Visual Hub -->
    <div class="visual-hub-static mb-8">
      <div class="visual-bg"></div>
      <v-icon :icon="icon" size="64" color="primary" class="visual-icon"></v-icon>
    </div>

    <div class="narrative-content-admin mx-auto">
      <h3 class="text-h5 font-weight-black text-slate-800 mb-3 text-center">{{ title }}</h3>
      <p class="text-body-1 text-slate-500 font-weight-bold mb-8 max-w-500 mx-auto text-center">
        {{ description }}
      </p>

      <div v-if="actionLabel" class="d-flex justify-center">
        <v-btn color="primary" variant="flat" class="admin-empty-action-btn rounded-lg px-8 font-weight-black"
          :prepend-icon="actionIcon" height="48" @click="$emit('action')">
          {{ actionLabel }}
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EmptyState',
  props: {
    title: { type: String, required: true },
    description: { type: String, required: true },
    icon: { type: String, default: 'mdi-folder-open-outline' },
    actionLabel: { type: String, default: '' },
    actionIcon: { type: String, default: 'mdi-plus' }
  },
  emits: ['action']
};
</script>

<style scoped>

.administrative-empty-state {
  font-family: 'Almarai', sans-serif !important;
}

.visual-hub-static {
  position: relative;
  width: 140px;
  height: 140px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.visual-bg {
  position: absolute;
  inset: 0;
  background: #f1f5f9;
  border-radius: 40px;
  transform: rotate(45deg);
}

.visual-icon {
  position: relative;
  z-index: 1;
}

.admin-empty-action-btn {
  text-transform: none !important;
  letter-spacing: 0 !important;
  box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2) !important;
}

.max-w-500 {
  max-width: 500px;
}

.text-slate-800 {
  color: #1e293b;
}

.text-slate-500 {
  color: #64748b;
}
</style>
