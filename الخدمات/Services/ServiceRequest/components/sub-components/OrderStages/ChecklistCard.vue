<template>
  <v-card variant="flat" class="checklist-suite-premium rounded-2xl border-system overflow-hidden">
    <!-- Section Header -->
    <div class="suite-header-premium px-4 px-md-6 py-4 py-md-5">
      <div class="d-flex align-center justify-space-between mb-4">
        <div class="d-flex align-center ga-2 ga-md-3">
          <div class="header-icon-shell d-none d-sm-flex">
            <v-icon icon="mdi-shield-check-outline" size="20" color="primary"></v-icon>
          </div>
          <div>
            <h3 class="text-subtitle-1 font-weight-black text-slate-900 mb-0">قائمة المتطلبات</h3>
          </div>
        </div>
        <v-btn v-if="!disabled_list" color="primary" variant="tonal"
          class="prime-note-btn rounded-lg px-3 px-sm-6 font-weight-black" height="34" prepend-icon="mdi-pencil-plus"
          @click="dialog.show = true">
          إضافة <span class="d-none d-sm-inline">متطلب</span>
        </v-btn>
      </div>

      <!-- Tactical Counter Bar -->
      <div
        class="tactical-counter-bar pa-2 pa-md-3 rounded-xl d-flex align-center justify-space-between flex-wrap ga-2">
        <div class="d-flex align-center ga-2 ga-md-4">
          <div class="counter-item">
            <span class="label">البنود:</span>
            <span class="value">{{ checkList?.length }}</span>
          </div>
          <v-divider vertical class="mx-0 mx-md-1 mt-1" length="10"></v-divider>
          <div class="counter-item">
            <span class="label">تم:</span>
            <span class="value text-success">{{ completedCount }}</span>
          </div>
        </div>
        <div class="d-flex align-center ga-1 ga-md-2 ml-sm-0 ml-auto">
          <span class="text-tiny font-weight-black text-slate-500 d-none d-sm-inline">معدل الثقة:</span>
          <div class="mini-progress-track">
            <div class="mini-progress-fill" :style="{ width: completionRate + '%' }"></div>
          </div>
          <span class="text-tiny font-weight-black text-primary">{{ completionRate }}%</span>
        </div>
      </div>
    </div>

    <!-- Requirements Grid -->
    <div class="suite-body px-4 py-2">
      <div v-if="checkList?.length" class="checklist-list-tactical">
        <div v-for="item in checkList" :key="item.id"
          :class="['requirement-node-executive', { 'is-checked': item.is_checked, 'is-disabled': disabled_list }]"
          @click="toggleItem(item)">
          <div class="node-executive-square">
            <v-icon :icon="item.is_checked ? 'mdi-check-bold' : ''" :size="12" class="check-mark"></v-icon>
          </div>
          <div class="node-content ml-6 flex-grow-1">
            <div class="d-flex align-center justify-space-between">
              <div class="node-text text-truncate">{{ item.name || item.title }}</div>
              <v-chip v-if="item.is_checked" size="x-small" color="success" variant="tonal"
                class="verified-tag shrink-0 ml-4">
                <v-icon start icon="mdi-shield-check" size="10"></v-icon>
                مكتمل
              </v-chip>
            </div>
          </div>
          <v-btn v-if="!disabled_list" icon="mdi-close-circle-outline" variant="text" color="slate-200" size="x-small"
            class="delete-action-btn ml-2" @click.stop="confirmDelete(item)"></v-btn>
        </div>
      </div>

      <div v-else class="empty-notion-premium py-8 text-center">
        <v-icon icon="mdi-playlist-star" size="32" color="slate-200" class="mb-2"></v-icon>
        <h4 class="text-caption font-weight-bold text-slate-400">لا توجد سجلات</h4>
      </div>
    </div>
  </v-card>

  <!-- Elite Requirement Portal (NoteModal Style) -->
  <v-dialog v-model="dialog.show" max-width="540" persistent no-click-animation class="master-portal-logic" scrollable>
    <v-card class="portal-surface rounded-xl overflow-hidden shadow-2xl">
      <!-- Elite Header Section -->
      <div class="portal-header pa-6 pa-md-8">
        <div class="d-flex align-center justify-space-between">
          <div class="d-flex align-center ga-4">
            <div class="portal-icon-box">
              <v-icon color="primary" size="24">mdi-playlist-plus</v-icon>
            </div>
            <div class="portal-title-logic">
              <h3 class="portal-h3">تعريف متطلب جديد</h3>
              <div class="portal-sub">بروتوكول الاعتماد والتوثيق</div>
            </div>
          </div>
          <v-btn icon="mdi-close" variant="text" color="slate-400" size="small" class="rounded-lg"
            @click="dialog.show = false" />
        </div>
      </div>

      <v-divider class="portal-sep" />

      <v-card-text class="pa-6 pa-md-8">
        <!-- Input Area -->
        <div class="documentation-arena mb-6">
          <label class="arena-label d-block mb-2">عنوان البند الرئيسي</label>
          <v-text-field v-model="dialog.title" placeholder="مثال: مراجعة المستندات الأصلية وتدقيقها" variant="outlined"
            hide-details color="primary" class="portal-input"></v-text-field>
        </div>

        <div class="documentation-arena">
          <label class="arena-label d-block mb-2">الشرح الفني (اختياري)</label>
          <v-textarea v-model="dialog.description" placeholder="أدخل الشرح التوضيحي لمعايير القبول لهذا البند..."
            variant="outlined" rows="4" auto-grow hide-details color="primary" class="portal-textarea"></v-textarea>
        </div>
      </v-card-text>

      <v-divider class="portal-sep" />

      <!-- Action Cluster -->
      <v-card-actions class="pa-6 pa-md-8 bg-slate-50/50">
        <v-btn variant="text" color="slate-500" class="px-6 font-weight-bold" height="44" @click="dialog.show = false">
          إلغاء
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="primary" variant="flat" class="px-10 rounded-lg font-weight-black elevation-4" height="44"
          :loading="dialog.loading" :disabled="!dialog.title || !dialog.title.trim()" @click="saveCheckList">
          اعتماد وحفظ
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <BaseConfirm v-model="del_con.show" :title="`حذف المتطلب`" :message="`هل أنت متأكد من حذف '${del_con.title}'؟`"
    type="error" :loading="loading.del_btn" @confirm="deleteCheck"></BaseConfirm>
</template>

<script>
export default {
  name: "ChecklistCard",
  inject: ["checkStagesActionPermission"],
  props: {
    items: { type: Array, default: () => [] },
    stage_id: { type: Number, default: null },
    title: { type: String, default: "قائمة التحقق والاعتماد" },
    disabled_list: { type: Boolean, default: false },
  },
  data() {
    return {
      url: "d-services/request-actions/",
      url_delete_list: "",

      checksList: [],
      loading: {},
      dialog: {},
      del_con: { show: false },
    };
  },
  created() {
    this.getCheckList();
  },
  computed: {
    checkList() {
      return this.checksList?.length ? this.checksList : this.items;
    },
    stageID() {
      return this.stage_id;
    },
    completedCount() {
      return this.checkList?.filter((i) => i.is_checked)?.length;
    },
    completionRate() {
      if (!this.checkList?.length) return 0;
      return Math.round((this.completedCount / this.checkList.length) * 100);
    }
  },
  methods: {
    openDel(item, index) {
      this.del_con.title = item?.title;
      this.del_con.index = index;
      this.del_con.check_id = item?.id;
      this.del_con.show = true;
    },
    openDia(item) {
      this.dialog = {};
      this.dialog.show = true;
    },
    async getCheckList() {
      try {
        // this.loading = true;
        await this.$axios(this.url + `${this.stage_id}/checklist/`).then(
          (response) => {
            this.checksList = response?.data?.data?.items;
          }
        );
      } finally {
        // this.loading = false;
      }
    },
    async deleteCheck() {
      try {
        this.loading.del_btn = true;
        await this.$axios
          ?.delete(
            this.url +
            `${this.stage_id}/checklist-delete/${this.del_con?.check_id}/`
          )
          .then((response) => {
            this.getCheckList();
            this.del_con.show = false;
            this.$snack("delete", { message: response?.data?.message });
          });
      } finally {
        this.loading.del_btn = false;
      }
    },
    async saveCheckList() {
      try {
        this.dialog.loading = true;
        await this.$axios
          ?.post(this.url + `${this.stage_id}/checklist-add/`, {
            title: this.dialog?.title,
            description: this.dialog?.description,
          })
          .then((response) => {
            this.getCheckList();
            this.dialog.show = false;
            this.dialog.title = "",
            this.dialog.description = ""
          });
      } finally {
        this.dialog.loading = false;
      }
    },
    handleCheck(item) {
      item.is_checking = true;
      this.updateCheckedList(item);
    },
    confirmDelete(item) {
      this.del_con.title = item?.name || item?.title;
      this.del_con.check_id = item?.id;
      this.del_con.show = true;
    },
    toggleItem(item) {
      if (this.disabled_list || item.is_checking) return;
      // const canUncheck = this.checkStagesActionPermission('CHECKLIST_UNCHECK');
      // const canCheck = this.checkStagesActionPermission('CHECKLIST_CHECK');

      // if (item.is_checked && !canUncheck) return;
      // if (!item.is_checked && !canCheck) return;
      item.is_checking = true;
      this.updateCheckedList(item);
    },
    async updateCheckedList(item) {
      try {
        await this.$axios
          ?.post(
            this.url +
            `${this.stage_id}/checklist-${item?.is_checked ? "uncheck" : "check"
            }/${item?.id}/`
          )
          .then((res) => {
            Object?.assign(item, res?.data?.data);
            // this.$snack("update", { message: res?.data?.message });
          })
          .catch(() => {
            this.getCheckList();
          });
      } finally {
        item.is_checking = false;
      }
    },
  },
};
</script>

<style scoped>
.checklist-suite-premium {
  background: white;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02) !important;
}

.suite-header-premium {
  background:
    radial-gradient(at 0% 0%, rgba(var(--v-theme-primary), 0.03) 0, transparent 50%),
    #ffffff;
  border-bottom: 1px solid #f1f5f9;
}

.header-icon-shell {
  width: 40px;
  height: 40px;
  background: white;
  border: 1px solid rgba(var(--v-theme-primary), 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(var(--v-theme-primary), 0.05);
}

.prime-note-btn {
  font-size: 11px !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
}

.tactical-counter-bar {
  background: #f8fafc;
  border: 1px solid #f1f5f9;
}

.counter-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.counter-item .label {
  font-size: 10px;
  font-weight: 800;
  color: #94a3b8;
}

.counter-item .value {
  font-size: 12px;
  font-weight: 900;
  color: #475569;
}

.mini-progress-track {
  width: 60px;
  height: 4px;
  background: #e2e8f0;
  border-radius: 10px;
  overflow: hidden;
}

.mini-progress-fill {
  height: 100%;
  background: rgb(var(--v-theme-primary));
  border-radius: 10px;
}

.checklist-list-tactical {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding-bottom: 12px;
}

.requirement-node-executive {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background: white;
  border-radius: 16px;
  cursor: pointer;
  border: 1px solid #f8fafc;
  margin-bottom: 2px;
}

@media (max-width: 600px) {
  .requirement-node-executive {
    padding: 10px 12px;
    border-radius: 12px;
  }
}

@media (min-width: 600px) {
  .requirement-node-executive {
    padding: 16px 24px;
  }
}

.requirement-node-executive:hover {
  background: #fbfcfe;
  border-color: rgba(var(--v-theme-primary), 0.15);
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.05);
}

.node-executive-square {
  width: 20px;
  height: 20px;
  border-radius: 6px;
  border: 2px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  background: white;
  flex-shrink: 0;
  margin-inline-end: 10px;
}

.requirement-node-executive.is-checked .node-executive-square {
  background: #10b981;
  border-color: #10b981;
  box-shadow: 0 0 12px rgba(16, 185, 129, 0.3);
}

.requirement-node-executive.is-checked .check-mark {
  color: white !important;
}

.node-text {
  font-size: 13.5px;
  font-weight: 800;
  color: #475569;
  letter-spacing: -0.01em;
}

@media (max-width: 600px) {
  .node-text {
    font-size: 12px;
  }

  .node-executive-square {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    margin-inline-end: 8px;
  }

  .node-content {
    margin-left: 0 !important;
  }
}

.requirement-node-executive.is-checked .node-text {
  color: #1e293b;
  opacity: 0.6;
  text-decoration: line-through;
}

.verified-tag {
  height: 20px !important;
  font-size: 10px !important;
  font-weight: 800 !important;
  border-radius: 6px !important;
}

.delete-action-btn {
  opacity: 0;
  transition: all 0.2s ease;
  color: #cbd5e1 !important;
}

.requirement-node-executive:hover .delete-action-btn {
  opacity: 1;
}

.text-tiny {
  font-size: 10px;
}

.requirement-node-executive.is-disabled {
  pointer-events: none;
  opacity: 0.5;
}

/* Master Portal Styles (NoteModal Parity) */
.master-portal-logic {
  font-family: 'Almarai', sans-serif;
}

.portal-surface {
  background: #ffffff;
}

.portal-header {
  background: #ffffff;
}

.portal-icon-box {
  width: 48px;
  height: 48px;
  background: #f1f5f9;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e2e8f0;
}

.portal-h3 {
  font-size: 1.1rem;
  font-weight: 900;
  color: #0f172a;
  margin-bottom: 2px;
}

.portal-sub {
  font-size: 10px;
  font-weight: 800;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.documentation-arena {
  width: 100%;
}

.arena-label {
  font-size: 13px;
  font-weight: 800;
  color: #475569;
}

.portal-input :deep(.v-field__outline),
.portal-textarea :deep(.v-field__outline) {
  --v-field-border-opacity: 0.1;
  border-radius: 10px !important;
}

.portal-sep {
  border-color: #f1f5f9 !important;
}

@media (max-width: 600px) {
  .master-portal-logic :deep(.v-overlay__content) {
    margin: 12px !important;
    width: calc(100% - 24px) !important;
  }
}
</style>
