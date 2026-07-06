<template>
  <div class="discount-manager-premium">
    <div class="discount-core-matrix">
      <!-- Top Status Indicator (Mobile/Seamless) -->
      <div class="d-flex justify-end mb-4 d-md-none">
        <v-chip :color="getStatusColor(discountData.discount_status)" variant="flat" size="small"
          class="font-weight-black">
          {{ getStatusLabel(discountData.discount_status) }}
        </v-chip>
      </div>

      <!-- Main Content -->
      <div v-if="discountData.discount_status !== 'no_discount'" class="discount-content-body">
        <div class="data-pulse-grid mb-8">
          <!-- Amount Before -->
          <div class="data-unit">
            <div class="unit-label">المبلغ قبل تطبيق التسوية</div>
            <div class="unit-value">
              <v-avatar size="24" color="slate-100" class="ml-2">
                <v-icon size="14" color="slate-500">mdi-text-box-outline</v-icon>
              </v-avatar>
              {{ formatCurrency(totalFee) }}
            </div>
          </div>

          <!-- Reason -->
          <div v-if="isVisible('discount_reason')" class="data-unit">
            <div class="unit-label">توصيف سبب الخصم</div>
            <div class="unit-value">
              <v-avatar size="24" color="amber-lighten-5" class="ml-2">
                <v-icon size="14" color="amber-darken-3">mdi-comment-text-outline</v-icon>
              </v-avatar>
              <span class="text-truncate">{{ discountData.discount_reason || "---" }}</span>
            </div>
          </div>

          <!-- Discount Amount -->
          <div v-if="isVisible('discount_amount')" class="data-unit highlight-amber">
            <div class="unit-label">قيمة التخفيض المعتمد</div>
            <div class="unit-value amber-darken-4">
              {{ formatCurrency(discountData.discount_amount) }}
              <span class="text-caption mr-2 font-weight-black">({{ calculatePercentage(discountData.discount_amount)
              }}%)</span>
            </div>
          </div>

          <!-- Dynamic Status Card (Desktop Only) -->
          <div class="data-unit d-none d-md-flex align-center justify-center">
            <div class="unified-status-box" :style="{ '--color': getHexColor(discountData.discount_status) }">
              <v-icon :icon="getStatusIcon(discountData.discount_status)" size="20" class="ml-2"></v-icon>
              <span class="font-weight-black">{{ getStatusLabel(discountData.discount_status) }}</span>
            </div>
          </div>
        </div>

        <!-- Metadata Footer -->
        <div v-if="isVisible('discount_at')" class="metadata-premium mb-6">
          <div class="d-flex align-center ga-2">
            <v-avatar size="28" color="slate-100">
              <v-icon size="16" color="slate-400">mdi-account-check-outline</v-icon>
            </v-avatar>
            <span class="text-caption text-slate-500">
              تمت الإضافة بواسطة
              <span class="font-weight-black text-slate-900">{{ discountData.discount_by__username }}</span>
              في
              <span class="font-weight-bold">{{ discountData.discount_at }}</span>
            </span>
          </div>
        </div>

        <!-- Alerts -->
        <div v-if="isVisible('discount_rejected_reason') || isVisible('discount_canceled_reason')" class="mb-8">
          <div :class="['alert-premium', discountData.discount_status === 'rejected' ? 'error' : 'warning']">
            <v-icon class="alert-icon-premium">{{ discountData.discount_status === "rejected" ? "mdi-alert-decagram" :
              "mdi-cancel" }}</v-icon>
            <div class="alert-content-premium">
              <div class="alert-title-premium">
                <span v-if="discountData.discount_status === 'rejected'">تم رفض الخصم</span>
                <span v-else>تم إلغاء الخصم</span>
              </div>
              <div class="alert-text-premium">{{ discountData.discount_rejected_reason ||
                discountData.discount_canceled_reason }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div v-if="!['no_discount', 'rejected', 'cancelled'].includes(discountData.discount_status)"
        class="actions-premium">
        <div class="d-flex flex-wrap ga-3">
          <v-btn v-if="checkActionPermission('APPROVE_DISCOUNT')" color="success" variant="flat"
            class="flex-grow-1 action-btn-premium" :loading="loading.approve" @click="handleApprove">
            <v-icon start size="18">mdi-check-decagram</v-icon>
            اعتماد الخصم
          </v-btn>

          <v-btn v-if="checkActionPermission('UPDATE_DISCOUNT')" color="amber-darken-3" variant="tonal"
            class="flex-grow-1 action-btn-premium" @click="openActionDialog('update')">
            <v-icon start size="18">mdi-pencil-outline</v-icon>
            تعديل
          </v-btn>

          <v-btn v-if="checkActionPermission('REJECT_DISCOUNT') && discountData?.discount_status=='pending'" color="error" variant="tonal"
            class="action-btn-premium" @click="openActionDialog('reject')">
            رفض الخصم
          </v-btn>

          <v-btn v-if="checkActionPermission('CANCEL_DISCOUNT')" color="slate-400" variant="text"
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
            <v-form ref="actionForm">
              <template v-if="dialog.type === 'update'">
                <div class="form-label-premium mb-2">نسبة الخصم</div>
                <v-text-field v-model.number="form.discount_percentage" type="number" variant="outlined"
                  density="comfortable" append-inner-icon="mdi-percent" placeholder="0.00" class="mb-4 rounded-xl"
                  :rules="[$max_value(100),$min_value(1)]" />

                <div class="calc-summary-premium mb-6 pa-4 rounded-xl border-dashed">
                  <div class="d-flex justify-space-between mb-2">
                    <span class="text-caption text-slate-500">المبلغ الأصلي:</span>
                    <span class="text-caption font-weight-bold">{{ formatCurrency(totalFee) }}</span>
                  </div>
                  <div class="d-flex justify-space-between mb-2">
                    <span class="text-caption text-slate-500">قيمة الخصم:</span>
                    <span class="text-caption font-weight-bold text-amber-darken-3"> {{
                      formatCurrency(form.discount_amount) }}</span>
                  </div>
                  <v-divider class="my-2"></v-divider>
                  <div class="d-flex justify-space-between">
                    <span class="text-subtitle-2 font-weight-black">المبلغ بعد الخصم:</span>
                    <span class="text-subtitle-2 font-weight-black text-success">{{ formatCurrency(totalFee -
                      (form.discount_amount || 0)) }}</span>
                  </div>
                </div>

                <div class="form-label-premium mb-2">سبب الخصم</div>
                <v-textarea v-model="form.discount_reason" placeholder="يرجى توضيح سبب منح الخصم..." variant="outlined"
                  rows="3" class="rounded-xl" :rules="[$required]" />
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
            <v-btn color="amber-darken-3" variant="flat" class="rounded-xl px-8 font-weight-black text-white"
              height="44" :loading="loading.submit" @click="handleActionSubmit">تأكيد الإجراء</v-btn>
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
  name: "DiscountManager",
  inject: ["context", "checkActionPermission"],
  props: {
    initialDiscountData: { type: Object, default: () => ({ discount_status: "no_discount" }) },
  },
  emits: ["updated"],
  data() {
    return {
      url: this.context.url,
      requestId: this.context.request_id,
      loading: { approve: false, submit: false },
      snackbar: { show: false, text: "", color: "success" },
      dialog: { show: false, type: "", title: "" },
      form: { discount_amount: null, discount_percentage: null, discount_reason: "", reason: "" },
    };
  },
  computed: {
    requestDetails(){
      return this.context?.request_details
    },
    requestId() {
      return this.context?.request_id;
    },
    discountData() {
      return this.context?.request_details &&
        this.context.request_details.discount_status
        ? this.context.request_details
        : this.initialDiscountData;
    },
    totalFee() {
      return this.context?.request_details?.total_fee || 0;
    },
    calculatedAmount() {
      // if (!this.form.discount_percentage || !this.totalFee) return 0;
      // return (this.form.discount_percentage / 100) * this.totalFee;
      return this.form.discount_amount || 0;
    },
    calculatedDiscountValue() {
      // if (!this.discountData.discount_amount || !this.totalFee) return 0;
      // return (this.discountData.discount_amount / 100) * this.totalFee;
      return this.discountData.discount_amount || 0;
    },
    calculatedFeeAfterDiscount() {
      return Math.max(0, this.totalFee - this.calculatedDiscountValue);
    },
    currencyName() {
      return this.context?.request_details?.currency__data?.name_ar || "$";
    },
  },
  methods: {
    isVisible(field) {
      const status = this.discountData.discount_status;
      const visibility = {
        discount_reason: status !== "no_discount",
        discount_at: status !== "no_discount",
        discount_amount: ["pending", "approved"].includes(status),
        discounted_fee: ["pending", "approved"].includes(status),
        discount_rejected_reason: status === "rejected",
        discount_rejected_at: status === "rejected",
        discount_canceled_reason: status === "cancelled",
        discount_canceled_at: status === "cancelled",
      };
      return visibility[field] || false;
    },
    getStatusLabel(status) {
      const labels = {
        no_discount: "بدون خصم",
        pending: "قيد المراجعة",
        approved: "معتمد",
        rejected: "مرفوض",
        cancelled: "ملغى",
      };
      return labels[status] || status;
    },
    getStatusColor(status) {
      const colors = {
        no_discount: "slate-400",
        pending: "warning",
        approved: "success",
        rejected: "error",
        cancelled: "slate-500",
      };
      return colors[status] || "primary";
    },
    getStatusIcon(status) {
      const icons = {
        no_discount: "mdi-minus-circle-outline",
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
        this.dialog.title = "تعديل بيانات الخصم";
        this.form.discount_percentage = this.discountData.discount_percentage;
        this.form.discount_amount = this.discountData.discount_amount;
        this.form.discount_reason = this.discountData.discount_reason;
      } else {
        this.dialog.title = type === "cancel" ? "إلغاء الخصم" : "رفض الخصم";
      }
    },
    async handleApprove() {
      this.loading.approve = true;
      try {
        const res = await this.$axios.post(
          `/d-services/service-requests/${this.requestId}/approve-discount/`
        );
        const data = res.data.data || res.data;
        this.showFeedback("تم اعتماد الخصم بنجاح");
        // this.discountData = data;
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
      const { valid } = await this.$refs.actionForm.validate();
      if (valid) {
        this.loading.submit = true;
        const baseUrl = `/d-services/service-requests/${this.requestId}`;
        let endpoint = "",
          payload = {};
        if (this.dialog.type === "update") {
          endpoint = `${baseUrl}/update-discount/`;
          payload = {
            discount_percentage: this.form.discount_percentage,
            discount_reason: this.form.discount_reason,
          };
        } else if (this.dialog.type === "cancel") {
          endpoint = `${baseUrl}/cancel-discount/`;
          payload = { cancel_reason: this.form.reason };
        } else if (this.dialog.type === "reject") {
          endpoint = `${baseUrl}/reject-discount/`;
          payload = { reject_reason: this.form.reason };
        }
        try {
          const res = await this.$axios.post(endpoint, payload);
          const data = res.data.data || res.data;
          this.showFeedback("تمت العملية بنجاح");
          // this.discountData = data;
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
    calculatePercentage(amount) {
      if (!amount || !this.totalFee) return 0;
      return ((amount / this.totalFee) * 100).toFixed(2).replace(/\.00$/, "");
    },
    getHexColor(status) {
      const colors = {
        no_discount: "#64748b",
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
  background: #fdfdfd;
  border: 1px solid #e2e8f0;
  padding: 24px;
  border-radius: 20px;
}

.data-unit:hover {
  background: #ffffff;
  border-color: #fbbf24;
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

.amber-darken-4 {
  color: #92400e;
}

.highlight-amber {
  background: #fffbeb !important;
  border-color: #fef3c7 !important;
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
  border-right: 3px solid #fbd38d;
  background: #fffaf0;
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
