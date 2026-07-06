<template>
  <div class="workflow-master-frame border-system rounded-3xl bg-white shadow-2xl">
    <!-- Mobile Stage Header (Top Priority) -->
    <div class="d-block d-lg-none px-3 pt-3 pb-0">
      <StageHeader :selectedStage="selectedStage" />
    </div>

    <v-row no-gutters class="workflow-main-row">
      <!-- Navigational Pane -->
      <WorkflowSidebar
        :stages="actionSteps"
        :selected-id="selectedStage?.id"
        class="system-integrated-sidebar"
        title="مركز التحكم والعمليات"
        subtitle="نظام تتبع الموارد والقرار"
        icon="mdi-shield-crown"
        @select="selectStage"
      />

      <!-- Operational Workspace -->
      <v-col cols="12" md="8" lg="9" class="workflow-workspace-pane">
        <div :key="selectedStage?.id" class="workspace-scroll-area pa-3 pa-md-6 pa-lg-8">
          <!-- Integrated Header (Desktop Only) -->
          <div class="mb-4 mb-lg-8 d-none d-lg-block">
            <StageHeader :selectedStage="selectedStage" />
          </div>

          <v-row class="mt-0 mt-lg-6">
            <!-- Main Content Column -->
            <v-col cols="12" lg="8" class="d-flex flex-column ga-3 ga-lg-6">
              <!-- Checklist Section -->

              <ChecklistCard
                :items="selectedStage?.checklist_items"
                :stage_id="selectedStage?.id"
                :disabled_list="!selectedStage?.is_current"
              />

              <!-- Tabs Section: Notes & Files -->
              <v-card
                variant="flat"
                class="quantum-tabs-card rounded-2xl border-system overflow-hidden"
              >
                <div class="tabs-header-premium pa-1 pa-md-2 border-bottom">
                  <v-tabs
                    v-model="activeTab"
                    color="primary"
                    align-tabs="center"
                    hide-slider
                    class="compact-tabs"
                    density="compact"
                  >
                    <v-tab value="notes" class="rounded-xl px-2 px-md-6">
                      <v-icon
                        icon="mdi-comment-text-multiple-outline"
                        size="16"
                        class="ml-1 ml-md-2"
                      ></v-icon>
                      <span class="text-caption font-weight-black d-none d-sm-inline"
                        >سجل الملاحظات</span
                      >
                      <span class="text-caption font-weight-black d-sm-none"
                        >الملاحظات</span
                      >
                    </v-tab>
                    <v-tab value="files" class="rounded-xl px-2 px-md-6">
                      <v-icon
                        icon="mdi-folder-open-outline"
                        size="16"
                        class="ml-1 ml-md-2"
                      ></v-icon>
                      <span class="text-caption font-weight-black d-none d-sm-inline"
                        >الوثائق والمخرجات</span
                      >
                      <span class="text-caption font-weight-black d-sm-none"
                        >الوثائق</span
                      >
                    </v-tab>
                  </v-tabs>
                </div>

                <v-window v-model="activeTab">
                  <!-- Notes Tab -->
                  <v-window-item value="notes">
                    <div
                      class="pa-3 pa-md-6 bg-white overflow-auto scroll-premium"
                      style="max-height: 400px"
                    >
                      <LogEntryCard
                        :entry="{ ...selectedStage, notes: displayNotes }"
                        :topDetails="false"
                        @logEntry="noteDialog = true"
                      />
                    </div>
                  </v-window-item>

                  <!-- Files Tab -->
                  <v-window-item value="files">
                    <div class="pa-3 pa-md-6 pa-lg-10 bg-white" style="min-height: 250px">
                      <v-row class="ga-y-3 ga-y-md-6">
                        <v-col
                          v-if="checkStagesActionPermission('INPUT')"
                          cols="12"
                          sm="6"
                          md="12"
                          lg="6"
                        >
                          <div
                            class="file-action-modern input-modern"
                            @click="openDialog('input')"
                          >
                            <div class="icon-shell success">
                              <v-icon size="20">mdi-tray-arrow-down</v-icon>
                            </div>
                            <div class="content">
                              <h4 class="text-subtitle-2 font-weight-black">
                                استمارة المرحلة
                              </h4>
                              <p class="d-none d-sm-block">
                                تعبئة البيانات والوثائق المطلوبة
                              </p>
                            </div>
                            <v-icon
                              icon="mdi-chevron-left"
                              class="arrow-hint"
                              size="18"
                            ></v-icon>
                          </div>
                        </v-col>

                        <v-col
                          v-if="checkStagesActionPermission('OUTPUT')"
                          cols="12"
                          sm="6"
                          md="12"
                          lg="6"
                        >
                          <div
                            class="file-action-modern output-modern"
                            @click="openDialog('output')"
                          >
                            <div class="icon-shell warning">
                              <v-icon size="20">mdi-tray-arrow-up</v-icon>
                            </div>
                            <div class="content">
                              <h4 class="text-subtitle-2 font-weight-black">
                                مخرجات العمل
                              </h4>
                              <p class="d-none d-sm-block">
                                استعراض وتحميل النسخ النهائية
                              </p>
                            </div>
                            <v-icon
                              icon="mdi-chevron-left"
                              class="arrow-hint"
                              size="18"
                            ></v-icon>
                          </div>
                        </v-col>
                      </v-row>
                    </div>
                  </v-window-item>
                </v-window>
              </v-card>
            </v-col>

            <!-- Sidebar Info Column -->
            <v-col cols="12" lg="4" class="d-flex flex-column ga-3 ga-lg-6">
              <!-- Decision Center -->
              <DecisionCenter :selectedStage="selectedStage" />

              <!-- Execution Log / Assignee Card -->
              <AssigneeCard :selectedStage="selectedStage" />

              <!-- Inactive State Information -->
              <div
                v-if="
                  !selectedStage?.is_current &&
                  selectedStage?.stage_status !== 'completed'
                "
                class="locked-stage-premium pa-4 pa-md-8 rounded-2xl border-system text-center bg-white shadow-sm"
              >
                <div class="lock-visual mb-3">
                  <v-icon icon="mdi-lock-outline" size="24" color="slate-300"></v-icon>
                </div>
                <h5 class="text-caption font-weight-black text-slate-500 mb-1">
                  المرحلة بانتظار التفعيل
                </h5>
                <p class="text-tiny font-weight-bold text-slate-400 mb-0">
                  يرجى استكمال المتطلبات السابقة في مسار العمل لفتح هذه المرحلة.
                </p>
              </div>
            </v-col>
          </v-row>
        </div>
      </v-col>
    </v-row>
  </div>

  <!-- Professional Note Dialog -->
  <v-dialog v-model="noteDialog" max-width="520">
    <v-card class="rounded-2xl overflow-hidden border-0 shadow-2xl mx-4">
      <div class="dialog-premium-header pa-6 bg-slate-50 border-bottom">
        <div class="d-flex align-center justify-space-between">
          <div class="d-flex align-center ga-4">
            <v-avatar color="primary" variant="tonal" size="40" class="rounded-lg">
              <v-icon color="primary" size="20">mdi-comment-plus-outline</v-icon>
            </v-avatar>
            <div>
              <h3 class="text-h6 font-weight-black text-slate-900 mb-0">إضافة ملاحظة</h3>
              <div class="text-caption text-slate-500 font-weight-bold">
                توثيق ملاحظات العمل على المرحلة
              </div>
            </div>
          </div>
          <v-btn
            icon="mdi-close"
            variant="tonal"
            color="slate-400"
            size="small"
            class="rounded-lg"
            @click="noteDialog = false"
          />
        </div>
      </div>

      <v-card-text class="pa-6">
        <v-textarea
          v-model="notes"
          placeholder="اكتب ملاحظاتك أو توجيهاتك هنا..."
          variant="outlined"
          rows="4"
          auto-grow
          color="primary"
          hide-details
          class="custom-textarea-premium"
        />
      </v-card-text>

      <v-card-actions class="pa-6 pt-0">
        <v-spacer />
        <v-btn
          variant="text"
          color="slate-500"
          class="px-6 font-weight-bold"
          @click="noteDialog = false"
        >
          إلغاء
        </v-btn>
        <v-btn
          color="primary"
          variant="flat"
          class="px-8 rounded-xl font-weight-black"
          height="44"
          :loading="noteLoading"
          :disabled="!notes.trim()"
          @click="submitNote"
        >
          حفظ الملاحظة
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- Files Dialog -->
  <BaseDialog
    v-model="dialog.show"
    :title="dialog.title"
    maxWidth="60vw"
    maxHeight="90vh"
    :actions="false"
  >
    <div class="overflow-hidden pa-4">
      <OrderOutputsInput
        :file-key="`${dialog.type}_file`"
        :data="current_stage"
        :type="dialog.type"
        :url="url_action"
        :stage_id="current_stage?.id"
        :template="current_stage[`custom_${dialog.type}_template`]"
      />
    </div>
  </BaseDialog>
</template>

<script>
import WorkflowSidebar from "./sub-components/OrderStages/WorkflowSidebar.vue";
import StageHeader from "./sub-components/OrderStages/StageHeader.vue";
import ChecklistCard from "./sub-components/OrderStages/ChecklistCard.vue";
import DecisionCenter from "./sub-components/OrderStages/DecisionCenter.vue";
import AssigneeCard from "./sub-components/OrderStages/AssigneeCard.vue";
import LogEntryCard from "@/pages/Services/ServiceRequest/ServiceRecords/components/LogEntryCard";
import OrderOutputsInputVue from "./sub-components/OrderOutputsInput/OrderOutputsInput.vue";
import BaseDialog from "@/pages/Services/ServiceRequest/components/shared/BaseDialog";

export default {
  name: "OrderStages",
  components: {
    WorkflowSidebar,
    StageHeader,
    ChecklistCard,
    DecisionCenter,
    AssigneeCard,
    LogEntryCard,
    OrderOutputsInputVue,
    BaseDialog,
  },
  props: {
    stages: { type: Array, required: true },
  },
  provide() {
    return {
      stage_id: this.selectedStage?.id,
      selectedStage: this.selectedStage,
      checkStagesActionPermission: this.checkStagesActionPermission,
      getStagesStatus: this.getStagesStatus,
      files_data: this.files_data,
    };
  },
  inject: ["context"],
  emits: ["action", "stage-change", "chat"],
  data() {
    return {
      notes_list: [],
      stages_items: [],
      stages_available_actions: [],
      selected_stage_steps: [],

      current_stage: {},
      files_data: {
        stage_input_data: {},
        stage_output_data: {},
      },
      dialog: {},

      noteDialog: false,
      noteLoading: false,

      notes: "",
      activeTab: "notes",
      url_action: "d-services/request-actions/",
      url_notes: "d-services/request-actions/id/add-note/",
      url_get_stages: "d-services/workflow-stages/",
      url_get_stages_steps: "d-services/workflow-logs/stage-stats/",
      url_stages_status: "d-services/stage-actions-status/",
    };
  },

  created() {
    this.getStagesStatus();
    this.current_stage = this.selectedStage;
    this.formatNotes(this.selectedStage?.notes);
  },
  computed: {
    actionSteps() {
      return this.context?.request_details?.action_steps;
    },
    selectedStage() {
      if (!this.actionSteps || this.actionSteps.length === 0) return null;
      if (this.current_stage?.id) {
        const stage = this.actionSteps.find((s) => s.id === this.current_stage.id);
        if (stage) return stage;
      }
      return this.actionSteps.find((s) => s.is_current) || this.actionSteps[0];
    },
    stageQuickInfo() {
      return [
        {
          label: "تاريخ البدء",
          value: this.selectedStage?.startDate || "---",
          icon: "mdi-calendar-clock",
        },
        {
          label: "المدة الزمنية",
          value: this.selectedStage?.duration || "---",
          icon: "mdi-timer-sand",
        },
        {
          label: "مستوى الأولوية",
          value: this.selectedStage?.priority || "عادي",
          icon: "mdi-alert-decagram-outline",
        },
      ];
    },
    displayNotes() {
      return this.formatNotes(this.selectedStage?.notes) || [];
    },
  },
  methods: {
    async openDialog(type) {
      if (type == "output") {
        this.dialog.title = "المدخلات";
      } else {
        this.dialog.title = "المخرجات";
      }
      this.dialog.type = type;
      await this.getFilesData(type);
    },

    async getStagesStatus(empty_current) {
      if (!this.selectedStage?.id) return;
      await this.$axios(`${this.url_stages_status}${this.selectedStage?.id}/`).then(
        (res) => {
          this.stages_available_actions = res.data?.data?.available_actions ?? [];
          if (empty_current) {
            this.current_stage = {};
          }
        }
      );
    },
    async getFilesData(type) {
      try {
        await this.$axios(
          `${this.url_action}${this.selectedStage?.id}/${type}-data/`
        ).then((res) => {
          this.files_data[`stage_${type}_data`] = res?.data?.data?.template_data;
          console.log("files", this.files_data);

          this.dialog.show = true;
        });
      } catch (error) {
        console.log(error);
      }
    },
    checkStagesActionPermission(action) {
      return (
        this.stages_available_actions?.some(
          (action_perm) =>
            action_perm.action === action?.toUpperCase() &&
            action_perm.has_permission == true
        ) || false
      );
    },
    selectStage(stage) {
      this.current_stage = stage;
      console.log(this.current_stage);
      this.getStagesStatus();
    },
    async submitNote() {
      try {
        this.noteLoading = true;
        await this.$axios
          ?.post(`${this.url_notes}`?.replace("id", this.selectedStage?.id), {
            notes: this.notes,
          })
          .then((res) => {
            const data = res?.data;
            this.$snack("add", { message: res?.data?.message });
            this.notes = "";
            this.context.getRequestDetails();
          });
      } catch (error) {
      } finally {
        this.noteLoading = false;
        this.noteDialog = false;
      }
    },
    formatNotes(notes) {
      if (!notes) {
        if (this.selectStage) this.selectStage.notes = [];
        return;
      }

      let notesToProcess = [];
      if (Array.isArray(notes)) {
        notesToProcess = notes;
      } else if (typeof notes === "string") {
        notesToProcess = notes.split("\n&..");
      } else {
        return;
      }

      const formatted = notesToProcess
        .map((n) => {
          if (!n) return null;

          if (typeof n === "object" && n !== null && (n.text || n.notes)) {
            return n;
          }

          if (typeof n === "string") {
            const trimmed = n.trim();
            if (!trimmed) return null;

            const splitted = trimmed.split("");
            if (
              splitted.length >= 4 &&
              splitted[0].startsWith("[") &&
              splitted[1].endsWith("]")
            ) {
              return {
                time: `${splitted[0].slice(1)} ${splitted[1].slice(0, -1)}`,
                user: splitted[2],
                text: splitted.slice(3).join(" "),
              };
            }
            return {
              time: "---",
              user: "النظام",
              text: trimmed,
            };
          }
          return null;
        })
        .filter(Boolean);
      return formatted;
    },
  },
};
</script>

<style scoped>
.workflow-master-frame {
  min-height: 85vh;
  background: #ffffff;
}

.workflow-main-row {
  display: flex;
  flex-wrap: nowrap;
  height: 100%;
}

.workflow-workspace-pane {
  height: 90vh;
  overflow-y: auto;
  scrollbar-width: thin;
  position: relative;
  background: radial-gradient(
      at 0% 0%,
      rgba(var(--v-theme-primary), 0.05) 0,
      transparent 50%
    ),
    radial-gradient(at 100% 0%, rgba(var(--v-theme-primary), 0.03) 0, transparent 40%),
    #f8fafc;
}

@media (max-width: 960px) {
  .workspace-scroll-area {
    padding: 0 !important;
    margin: 0 !important;
    width: 100% !important;
  }

  .workflow-workspace-pane {
    background: #f8fafc !important;
    /* Flat background for better performance on mobile */
  }
}

.workspace-scroll-area {
  max-width: 1400px;
  margin: 0 auto;
}

@media (max-width: 960px) {
  .workflow-main-row {
    flex-wrap: wrap;
  }

  .workflow-workspace-pane {
    height: auto !important;
    min-height: auto !important;
    overflow-y: visible !important;
    border-right: none;
    padding-bottom: 80px !important;
    /* Safe area for bottom actions */
  }

  .workflow-master-frame {
    border-radius: 0 !important;
    min-height: auto !important;
    height: auto !important;
    overflow: visible !important;
    box-shadow: none !important;
    border: none !important;
  }
}

.ga-6 {
  gap: 24px !important;
}

/* Module Styling */
.quantum-tabs-card {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
}

.tabs-header-premium {
  background: #f8fafc;
  border-bottom: 1px solid #f1f5f9;
}

.compact-tabs :deep(.v-tab) {
  text-transform: none !important;
  letter-spacing: 0 !important;
  font-weight: 800;
  color: #64748b;
  transition: all 0.3s ease;
}

.compact-tabs :deep(.v-tab--selected) {
  background: #ffffff;
  color: #2563eb;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08);
}

.file-action-modern {
  display: flex;
  align-items: center;
  padding: 24px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  cursor: pointer;
  position: relative;
}

.file-action-modern:hover {
  background: #ffffff;
  border-color: #2563eb;
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.05);
}

.icon-shell {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 12px;
  flex-shrink: 0;
}

@media (min-width: 960px) {
  .icon-shell {
    width: 48px;
    height: 48px;
    border-radius: 12px;
  }
}

.icon-shell.success {
  background: #f0fdf4;
  color: #10b981;
}

.icon-shell.warning {
  background: #fffbe8;
  color: #d97706;
}

.content h4 {
  font-size: 15px;
  font-weight: 900;
  color: #1e293b;
  margin-bottom: 4px;
}

.content p {
  font-size: 12px;
  color: #64748b;
  margin: 0;
  font-weight: 600;
}

.arrow-hint {
  margin-right: auto;
  opacity: 0;
  transform: translateX(10px);
  transition: all 0.3s ease;
  color: #2563eb;
}

.file-action-modern:hover .arrow-hint {
  opacity: 1;
  transform: translateX(0);
}

@media (max-width: 600px) {
  .file-action-modern {
    padding: 12px;
    border-radius: 16px;
  }

  .icon-shell {
    width: 36px;
    height: 36px;
    margin-left: 10px;
  }
}

.locked-stage-premium {
  border: 2px dashed #e2e8f0 !important;
  background: #f8fafc !important;
}

.border-system {
  border: 1px solid #e2e8f0 !important;
}

.border-bottom {
  border-bottom: 1px solid #f1f5f9 !important;
}

.ga-6 {
  gap: 24px;
}

.ga-y-6 {
  row-gap: 24px;
}
</style>
