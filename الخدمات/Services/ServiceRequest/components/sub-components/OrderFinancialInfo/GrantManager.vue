<template>
  <div class="grant-manager-premium">
    <div class="grant-core-matrix">
      <!-- Top Status Indicator (Mobile/Seamless) -->
      <div class="d-flex justify-end mb-4 d-md-none">
        <v-chip :color="getStatusColor(grantData.grant_status)" variant="flat" size="small" class="font-weight-black">
          {{ getStatusLabel(grantData.grant_status) }}
        </v-chip>
      </div>

      <!-- Main Content -->
      <div v-if="grantData.grant_status !== 'no_grant'" class="grant-content-body">
        <div class="data-pulse-grid mb-8">
          <!-- Grant Source -->
          <div v-if="isVisible('fk_grant_source')" class="data-unit">
            <div class="unit-label">مصدر التمويل المعتمد</div>
            <div class="unit-value">
              <v-avatar size="24" color="primary-lighten-5" class="ml-2">
                <v-icon size="14" color="primary">mdi-bank-outline</v-icon>
              </v-avatar>
              {{ grantData.fk_grant_source__name_ar || "---" }}
            </div>
          </div>

          <!-- Percentage -->
          <div v-if="isVisible('grant_percentage')" class="data-unit">
            <div class="unit-label">نسبة التغطية المالية</div>
            <div class="unit-value highlight-text primary">
              {{ grantData.grant_percentage }}%
              <span class="text-caption mr-1">من إجمالي الرسوم</span>
            </div>
          </div>

          <!-- Amount -->
          <div v-if="isVisible('grant_amount')" class="data-unit highlight-success">
            <div class="unit-label">إجمالي مبلغ المنحة</div>
            <div class="unit-value success">
              {{ formatCurrency(grantData.grant_amount) }}
            </div>
          </div>

          <!-- Dynamic Status Card (Desktop Only) -->
          <div class="data-unit d-none d-md-flex align-center justify-center">
            <div class="unified-status-box" :style="{ '--color': getHexColor(grantData.grant_status) }">
              <v-icon :icon="getStatusIcon(grantData.grant_status)" size="20" class="ml-2"></v-icon>
              <span class="font-weight-black">{{ getStatusLabel(grantData.grant_status) }}</span>
            </div>
          </div>
        </div>

        <!-- Metadata Footer -->
        <div v-if="isVisible('grant_assigned_at')" class="metadata-premium mb-6">
          <div class="d-flex align-center ga-2">
            <v-avatar size="28" color="slate-100">
              <v-icon size="16" color="slate-400">mdi-account-tie-outline</v-icon>
            </v-avatar>
            <span class="text-caption text-slate-500">
              تم التعيين بواسطة
              <span class="font-weight-black text-slate-900">{{ grantData.fk_requester__username }}</span>
              في
              <span class="font-weight-bold">{{ grantData.grant_assigned_at }}</span>
            </span>
          </div>
        </div>

        <!-- Alerts -->
        <div v-if="isVisible('grant_rejected_reason') || isVisible('grant_cancel_reason')" class="mb-8">
          <div :class="['alert-premium', grantData.grant_status === 'rejected' ? 'error' : 'warning']">
            <v-icon class="alert-icon-premium">{{ grantData.grant_status === "rejected" ? "mdi-alert-decagram" :
              "mdi-cancel" }}</v-icon>
            <div class="alert-content-premium">
              <div class="alert-title-premium">
                <span v-if="grantData.grant_status === 'rejected'">تم رفض المنحة</span>
                <span v-else>تم إلغاء المنحة</span>
              </div>
              <div class="alert-text-premium">{{ grantData.grant_rejected_reason || grantData.grant_cancel_reason }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div v-if="!['no_grant', 'rejected', 'cancelled'].includes(grantData.grant_status)" class="actions-premium">
        <div class="d-flex flex-wrap ga-3">
          <v-btn v-if="checkActionPermission('APPROVE_GRANT')" color="success" variant="flat"
            class="flex-grow-1 action-btn-premium" :loading="loading.approve" @click="handleApprove">
            <v-icon start size="18">mdi-check-decagram</v-icon>
            اعتماد المنحة
          </v-btn>

          <v-btn v-if="checkActionPermission('UPDATE_GRANT')" color="primary" variant="tonal"
            class="flex-grow-1 action-btn-premium" @click="openActionDialog('update')">
            <v-icon start size="18">mdi-pencil-outline</v-icon>
            تعديل
          </v-btn>

          <v-btn v-if="checkActionPermission('REJECT_GRANT')" color="error" variant="tonal"
            class="action-btn-premium" @click="openActionDialog('reject')">
            رفض المنحة
          </v-btn>

          <v-btn v-if="checkActionPermission('CANCEL_GRANT')" color="slate-400" variant="text"
            class="action-btn-premium" @click="openActionDialog('cancel')">
            إلغاء
          </v-btn>

        </div>
      </div>

      <!-- Professional Dialog -->
      <v-dialog v-if="dialog.show" v-model="dialog.show" max-width="500px">
        <v-card class="rounded-2xl overflow-hidden">
          <div class="dialog-header-premium pa-6 bg-slate-50 border-bottom">
            <h3 class="text-h6 font-weight-black text-slate-900 mb-0">{{ dialog.title }}</h3>
          </div>

          <v-card-text class="pa-6">
            <v-form ref="form">
              <template v-if="dialog.type === 'update'">
                <div class="form-label-premium mb-2">مصدر المنحة</div>
                <auto-list v-model="form.fk_grant_source" item-title="name" item-value="id" name="GrantSource"
                  :rules="[$required]" class="mb-4"></auto-list>

                <div class="form-label-premium mb-2">نسبة التغطية (%)</div>
                <v-text-field v-model.number="form.grant_percentage" type="number" variant="outlined"
                  density="comfortable" suffix="%" placeholder="0" class="mb-4 rounded-xl"
                  :rules="[(v) => (v >= 0 && v <= 100) || 'يجب أن تكون النسبة بين 0 و 100', $required]" />

                <div class="calc-summary-premium mb-2 pa-4 rounded-xl border-dashed">
                  <div class="d-flex justify-space-between mb-2">
                    <span class="text-caption text-slate-500">إجمالي الرسوم:</span>
                    <span class="text-caption font-weight-bold">{{ formatCurrency(totalFee) }}</span>
                  </div>
                  <div class="d-flex justify-space-between">
                    <span class="text-subtitle-2 font-weight-black">قيمة المنحة المتوقعة:</span>
                    <span class="text-subtitle-2 font-weight-black text-success">{{
                      formatCurrency(calculatedGrantAmount)
                    }}</span>
                  </div>
                </div>
              </template>

              <template v-if="['cancel', 'reject'].includes(dialog.type)">
                <div class="form-label-premium mb-2">سبب الإجراء</div>
                <v-textarea v-model="form.reason" placeholder="يرجى كتابة سبب الإجراء بالتفصيل..." variant="outlined"
                  rows="3" class="rounded-xl" :rules="[$required]" />
              </template>
            </v-form>
          </v-card-text>

          <v-card-actions class="pa-6 pt-0">
            <v-spacer />
            <v-btn variant="text" color="slate-400" class="font-weight-bold" @click="dialog.show = false">تراجع</v-btn>
            <v-btn color="primary" variant="flat" class="rounded-xl px-8 font-weight-black" height="44"
              :loading="loading.submit" @click="handleActionSubmit">تأكيد الإجراء</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-snackbar v-model="snackbar.show" :color="snackbar.color" rounded="lg">
        <div class="d-flex align-center ga-2">
          <v-icon size="20">mdi-information-outline</v-icon>
          <span class="font-weight-bold">{{ snackbar.text }}</span>
        </div>
      </v-snackbar>
    </div>
  </div>
</template>

<script>
export default {
  name: "GrantManager",
  inject: ["context", "checkActionPermission"],
  props: {
    initialGrantData: { type: Object, default: () => ({ grant_status: "no_grant" }) },
  },
  emits: ["updated"],
  data() {
    return {
      url: this.context.url,
      requestId: this.context.request_id,
      loading: { approve: false, submit: false },
      snackbar: { show: false, text: "", color: "success" },
      dialog: { show: false, type: "", title: "" },
      form: { fk_grant_source: null, grant_percentage: null, reason: "" },
    };
  },
  computed: {
    grantData() {
      return this.context?.request_details &&
        this.context.request_details.grant_status
        ? this.context.request_details
        : this.initialGrantData;
    },
    totalFee() {
      return this.context?.request_details?.total_fee || 0;
    },
    currencyName() {
      return this.context?.request_details?.currency__data?.name_ar || "$";
    },
    calculatedGrantAmount() {
      if (!this.form.grant_percentage || !this.totalFee) return 0;
      return (this.form.grant_percentage / 100) * this.totalFee;
    },
  },
  methods: {
    isVisible(field) {
      const status = this.grantData.grant_status;
      const visibility = {
        fk_grant_source: status !== "no_grant",
        grant_percentage: status !== "no_grant",
        grant_assigned_at: status !== "no_grant",
        grant_amount: status === "approved",
        grant_rejected_at: status === "rejected",
        grant_rejected_reason: status === "rejected",
        grant_cancel_at: status === "cancelled",
        grant_cancel_reason: status === "cancelled",
      };
      return visibility[field] || false;
    },
    getStatusLabel(status) {
      const labels = {
        no_grant: "بدون منحة",
        pending: "قيد المراجعة",
        approved: "معتمدة",
        rejected: "مرفوضة",
        cancelled: "ملغاة",
      };
      return labels[status] || status;
    },
    getStatusColor(status) {
      const colors = {
        no_grant: "slate-400",
        pending: "warning",
        approved: "success",
        rejected: "error",
        cancelled: "slate-500",
      };
      return colors[status] || "primary";
    },
    getStatusIcon(status) {
      const icons = {
        no_grant: "mdi-minus-circle-outline",
        pending: "mdi-clock-outline",
        approved: "mdi-check-decagram",
        rejected: "mdi-alert-circle",
        cancelled: "mdi-cancel",
      };
      return icons[status] || "mdi-information";
    },
    openActionDialog(type) {
      this.dialog.type = type;
      this.dialog.show = true;
      this.form.reason = "";
      if (type === "update") {
        this.dialog.title = "تعديل بيانات المنحة";
        this.form.fk_grant_source = this.grantData.fk_grant_source;
        this.form.grant_percentage = this.grantData.grant_percentage;
      } else {
        this.dialog.title = type === "cancel" ? "إلغاء المنحة" : "رفض المنحة";
      }
    },
    async handleApprove() {
      this.loading.approve = true;
      try {
        const res = await this.$axios.post(
          `/d-services/service-requests/${this.requestId}/approve-grant/`
        );
        const data = res.data.data || res.data;
        this.showFeedback("تم اعتماد المنحة بنجاح");
        // this.grantData = data;
        if (this.context?.getRequestDetails) {
          await this.context.getRequestDetails();
        }
        this.$emit("updated", data);
      } catch (e) {
        this.showFeedback(
          "فشل الاعتماد: " + (e.response?.data?.detail || "خطأ في النظام"),
          "error"
        );
      } finally {
        this.loading.approve = false;
      }
    },
    async handleActionSubmit() {
      const { valid } = await this.$refs.form.validate();
      if (valid) {
        this.loading.submit = true;
        const baseUrl = `/d-services/service-requests/${this.requestId}`;
        let endpoint = "",
          payload = {};
        if (this.dialog.type === "update") {
          endpoint = `${baseUrl}/update-grant/`;
          payload = {
            fk_grant_source: this.form.fk_grant_source,
            grant_percentage: this.form.grant_percentage,
          };
        } else if (this.dialog.type === "cancel") {
          endpoint = `${baseUrl}/cancel-grant/`;
          payload = { cancel_reason: this.form.reason };
        } else if (this.dialog.type === "reject") {
          endpoint = `${baseUrl}/reject-grant/`;
          payload = { reject_reason: this.form.reason };
        }
        try {
          const res = await this.$axios.post(endpoint, payload);
          const data = res.data.data || res.data;
          this.showFeedback("تمت العملية بنجاح");
          if (this.context?.getRequestDetails) {
            await this.context.getRequestDetails();
          }
          this.$emit("updated", data);
          this.dialog.show = false;
        } catch (e) {
          this.showFeedback(
            "خطأ: " + (e.response?.data?.detail || "فشلت العملية"),
            "error"
          );
        } finally {
          this.loading.submit = false;
        }
      }
    },
    showFeedback(text, color = "success") {
      this.snackbar.text = text;
      this.snackbar.color = color;
      this.snackbar.show = true;
    },
    formatCurrency(val) {
      const num = new Intl.NumberFormat("en-US").format(val || 0);
      return `${num} ${this.currencyName}`;
    },
    getHexColor(status) {
      const colors = {
        no_grant: "#64748b",
        pending: "#f59e0b",
        approved: "#10b981",
        rejected: "#ef4444",
        cancelled: "#64748b",
      };
      return colors[status] || "#2563eb";
    },
  },
};
</script>

<style scoped>
.data-pulse-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.data-unit {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  padding: 24px;
  border-radius: 20px;
}

.data-unit:hover {
  background: #ffffff;
  border-color: #3b82f6;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.03);
  transform: translateY(-2px);
}

.unit-label {
  font-size: 11px;
  font-weight: 800;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
}

.unit-value {
  font-size: 1.25rem;
  font-weight: 950;
  color: #0f172a;
  display: flex;
  align-items: center;
}

.unit-value.highlight-text.primary {
  color: #2563eb;
}

.unit-value.success {
  color: #10b981;
}

.highlight-success {
  background: #f0fdf4 !important;
  border-color: #dcfce7 !important;
}

.unified-status-box {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  background: white;
  border-radius: 14px;
  border: 2px solid var(--color);
  color: var(--color);
  font-size: 14px;
}

.metadata-premium {
  padding: 16px;
  border-right: 3px solid #e2e8f0;
  background: #f8fafc;
  border-radius: 0 12px 12px 0;
}

.alert-premium {
  border: none !important;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.action-btn-premium {
  border-radius: 16px !important;
  height: 48px !important;
}
</style>
