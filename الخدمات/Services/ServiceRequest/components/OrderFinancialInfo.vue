<template>
  <div class="financial-full-portal">
    <!-- Sovereign Panoramic Header -->
    <header class="sovereign-panoramic-header mb-4">
      <div class="panoramic-inner d-flex align-center justify-space-between px-12 py-2">
        <div class="d-flex align-center ga-3">
          <div class="prime-avatar-ring">
            <v-avatar color="primary" size="36" class="elevation-1 rounded-lg">
              <v-icon icon="mdi-shield-check-outline" size="18" color="white"></v-icon>
            </v-avatar>
          </div>
          <div class="identity-stack">
            <h1 class="portal-title">الإدارة المالية المركزية</h1>
          </div>
        </div>

        <div class="intel-matrix d-flex ga-6">
          <div class="intel-cell">
            <span class="cell-label">فئة العملة</span>
            <span class="cell-val text-uppercase">{{ currencyName }}</span>
          </div>
          <v-divider vertical color="slate-200" opacity="0.5" class="mx-2" />
          <div class="intel-cell">
            <span class="cell-label">حالة التحصيل</span>
            <span :class="['cell-val-status', paymentStatusColor]">{{ paymentStatusLabel }}</span>
          </div>
        </div>

      </div>
    </header>

    <div class="portal-content-matrix px-6 pb-8">
      <!-- Phase 1: Performance Metrics HUD -->
      <section class="metrics-hud mb-8">
        <v-row>
          <v-col v-for="card in summaryCards" :key="card.title" cols="12" sm="6" md="3">
            <StatCard v-bind="card" />
          </v-col>
        </v-row>
      </section>

      <!-- Phase 2: Financial Ledger (Installments) -->
      <v-row class="mb-8" v-if="request_details?.payment_status != 'free'">
        <v-col cols="12">
          <v-card variant="flat" class="ledger-monolith rounded-2xl overflow-hidden border-system shadow-soft">
            <div class="monolith-header pa-6 d-flex align-center bg-white border-bottom">
              <v-icon icon="mdi-calendar-range" color="primary" class="ml-4" size="24"></v-icon>
              <div>
                <h3 class="monolith-title">سجل المواعيد المالية للمتطلبات</h3>
                <span class="monolith-sub">المخطط الزمني الكامل للتسويات، الأقساط والتحصيل</span>
              </div>
            </div>
            <div class="monolith-body" v-if="installments?.length>0">
              <InstallmentsTable :items="installments" @pay="(item) => $emit('pay', item)"
                @edit="(item) => $emit('edit-installment', item)"
                @delete="(item) => $emit('delete-installment', item)" />
            </div>
            <div class="monolith-body" v-else>
              <InvoicesTable :items="request_details?.invoices_data" @pay="(item) => $emit('pay', item)"
                @edit="(item) => $emit('edit-installment', item)"
                @delete="(item) => $emit('delete-installment', item)" />
            </div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Phase 3: Institutional Grants -->
      <v-row class="mb-8">
        <v-col cols="12">
          <v-card variant="flat" class="hub-entry-card rounded-2xl pa-8 border-system shadow-soft bg-white">
            <div class="d-flex align-center mb-8">
              <div class="hub-icon-shell indigo">
                <v-icon icon="mdi-medal-outline" color="indigo" size="24"></v-icon>
              </div>
              <div class="mr-4">
                <h4 class="hub-title text-h5">إدارة المنح والتمويل الأكاديمي</h4>
                <span class="hub-hint text-body-1">مراقبة وتعديل مخصصات الدعم المالي المركزية لهذا الطلب</span>
              </div>
            </div>
            <GrantManager ref="grantManagerRef" :initial-grant-data="grantData"
              @updated="(data) => $emit('grant-updated', data)" />
          </v-card>
        </v-col>
      </v-row>

      <!-- Phase 4: Financial Discounts & Settlements -->
      <v-row>
        <v-col cols="12">
          <v-card variant="flat" class="hub-entry-card rounded-2xl pa-8 border-system shadow-soft bg-white">
            <div class="d-flex align-center mb-8">
              <div class="hub-icon-shell orange">
                <v-icon icon="mdi-brightness-percent" color="orange-darken-2" size="24"></v-icon>
              </div>
              <div class="mr-4">
                <h4 class="hub-title text-h5">مرصد الخصومات والتسويات المالية</h4>
                <span class="hub-hint text-body-1">إدارة التخفيضات الاستثنائية والتسويات المعتمدة</span>
              </div>
            </div>
            <DiscountManager ref="discountManagerRef" :initial-discount-data="discountData"
              @updated="(data) => $emit('discount-updated', data)" />
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Interactive Layer -->
    <BaseDialog ref="confirmDialog" />
    <BaseNotification ref="notification" />
  </div>
</template>

<script>
import StatCard from "./sub-components/OrderFinancialInfo/StatCard.vue";
import InstallmentsTable from "./sub-components/OrderFinancialInfo/InstallmentsTable.vue";
import GrantManager from "./sub-components/OrderFinancialInfo/GrantManager.vue";
import DiscountManager from "./sub-components/OrderFinancialInfo/DiscountManager.vue";

export default {
  name: "OrderFinancialInfo",
  components: {
    StatCard,
    InstallmentsTable,
    GrantManager,
    DiscountManager,
  },
  inject: ["context","getRequestDetails"],
  props: {
    financials: {
      type: Object,
      default: () => ({ total: 12500, paid: 5000, remaining: 7500 }),
    },
    installments: { type: Array, default: () => [] },
    grantData: { type: Object, default: () => ({ grant_status: "no_grant" }) },
    discountData: {
      type: Object,
      default: () => ({ discount_status: "no_discount" }),
    },
  },
  emits: [
    "pay",
    "add-installment",
    "edit-installment",
    "delete-installment",
    "grant-updated",
    "discount-updated",
  ],
  data() {
    return {
      url: this.context.url,
      requestId: this.context.request_id,
      // request_details:this.context?.request_details,
      is_loading:false,
    };
  },
  computed: {
    request_details(){
      return this.context?.request_details
    },
    currencyName() {
      return this.context?.request_details?.currency__data?.symbol || "$";
    },
    paymentStatusLabel() {
      const { total, paid } = this.financials;
      if (paid >= total && total > 0) return "مكتمل السداد";
      if (paid > 0) return "مدفوع جزئياً";
      return "بانتظار التحصيل";
    },
    paymentStatusColor() {
      const { total, paid } = this.financials;
      if (paid >= total && total > 0) return "text-white opacity-90";
      if (paid > 0) return "text-orange-200";
      return "text-slate-300";
    },
    summaryCards() {
      const { total, paid, remaining } = this.financials;
      const cards = [];

      cards.push({
        title: "إجمالي قيمة الطلب",
        value: total,
        currency: this.currencyName,
        icon: "mdi-bank-outline",
        color: "primary",
        hexColor: "#2563eb",
        trend: "الرسوم الأساسية المعتمدة",
      });

      cards.push({
        title: "المبالغ المحصلة",
        value: paid,
        currency: this.currencyName,
        icon: "mdi-cash-check",
        color: "success",
        hexColor: "#10b981",
        trend: `المتبقي: ${this.formatSimpleNumber(remaining)}`,
        showProgress: true,
        progressValue: total > 0 ? Math.round((paid / total) * 100) : 0,
        progressLabel: "من إجمالي الرسوم",
      });

      const isGrantActive = this.context?.request_details?.grant_status !== "no_grant";
      const grantLabels = {
        pending: "قيد المراجعة",
        approved: "منحة معتمدة",
        rejected: "منحة مرفوضة",
        cancelled: "منحة ملغاة",
      };
      const grantColors = {
        pending: "#f59e0b",
        approved: "#6366f1",
        rejected: "#ef4444",
        cancelled: "#64748b",
      };
      const grantAmount = this.context?.request_details?.grant_amount || 0;
      const grantPercentage = this.context?.request_details?.grant_percentage || this.calculatePercentage(grantAmount);

      cards.push({
        title: "المنحة",
        value: isGrantActive ? `${grantPercentage}%` : 'لايوجد',
        currency: isGrantActive ? `(${this.formatSimpleNumber(grantAmount)} ${this.currencyName})` : '',
        icon: isGrantActive ? 'mdi-medal-outline' : 'mdi-star-off',
        color: isGrantActive ? 'indigo' : 'blue-grey',
        hexColor: isGrantActive ? '#6366f1' : '#94a3b8',
        statusLabel: isGrantActive ? grantLabels[this.context?.request_details?.grant_status] : '',
        statusColor: isGrantActive ? grantColors[this.context?.request_details?.grant_status] : '',
        trend: isGrantActive ? 'منحة' : 'لم يتم الحصول على منحة',
      });


      const isDiscountActive = this.context?.request_details?.discount_status !== "no_discount";
      const discountLabels = {
        pending: "قيد المراجعة",
        approved: "خصم معتمد",
        rejected: "خصم مرفوض",
        cancelled: "خصم ملغى",
      };
      const discountColors = {
        pending: "#f59e0b",
        approved: "#10b981",
        rejected: "#ef4444",
        cancelled: "#64748b",
      };
      const discountAmount = this.context?.request_details?.discount_amount || 0;
      const discountPercentage = this.context?.request_details?.discount_percentage || this.calculatePercentage(discountAmount);
      const amountBefore = total;
      const amountAfter = total - discountAmount;
      ;

      cards.push({
        title: "الخصم",
        value: isDiscountActive ? `${discountPercentage}%` : 'لايوجد',
        currency: isDiscountActive ?  `(${this.formatSimpleNumber(discountAmount)} ${this.currencyName})` : '',
        icon: isDiscountActive ? 'mdi-tag-outline' : 'mdi-tag-off-outline',
        color: isDiscountActive ? 'orange' : 'blue-grey',
        hexColor: isDiscountActive ? '#97316' : '#94a3b8',
        statusLabel: isDiscountActive ? discountLabels[this.context?.request_details?.discount_status] : '',
        statusColor: isDiscountActive ? discountColors[this.context?.request_details?.discount_status] : '',
        trend: isDiscountActive ? `قبل ${this.formatSimpleNumber(amountBefore)} | بعد: ${this.formatSimpleNumber(amountAfter)}` : 'لم يتم تطبيق الخصم',
      });
      return cards;
    },
  },
  methods: {


    openGrantDialog(type = "assign") {
      this.$refs.grantManagerRef?.openActionDialog(type);
    },
    openDiscountDialog(type = "add") {
      this.$refs.discountManagerRef?.openActionDialog(type);
    },
    formatCurrency(val) {
      const num = new Intl.NumberFormat("en-US").format(val || 0);
      return `${num} ${this.currencyName}`;
    },
    formatSimpleNumber(val) {
      return new Intl.NumberFormat("en-US").format(val || 0);
    },
    calculatePercentage(amount) {
      const total = this.financials.total || 0;
      if (!amount || !total) return 0;
      return ((amount / total) * 100).toFixed(2).replace(/\.00$/, "");
    },
  },
};
</script>

<style scoped>

.financial-full-portal {
  font-family: 'Noto Sans Arabic', 'Plus Jakarta Sans', sans-serif;
  background-color: #fcfdfe;
  min-height: 100vh;
  width: 100%;
}

/* Panoramic Header - Ultra Compact Focus */
.sovereign-panoramic-header {
  background: #ffffff;
  position: relative;
  overflow: hidden;
  border-bottom: 1px solid #f1f5f9;
  border-radius: 0 0 16px 16px;
}

.panoramic-inner {
  position: relative;
  z-index: 5;
}

.portal-title {
  color: #0f172a;
  font-size: 1.15rem;
  font-weight: 900;
  letter-spacing: -0.01em;
}

.premium-badge {
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  color: #2563eb;
  padding: 4px 14px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 800;
  display: flex;
  align-items: center;
}

.portal-subtitle {
  color: #64748b;
  font-size: 0.95rem;
  font-weight: 600;
}

.prime-avatar-ring {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.intel-matrix {
  background: #f8fafc;
  padding: 10px 24px;
  border-radius: 18px;
  border: 1px solid #e2e8f0;
}

.intel-cell {
  text-align: center;
  min-width: 100px;
}

.cell-label {
  display: block;
  font-size: 10px;
  font-weight: 800;
  color: #64748b !important;
  text-transform: uppercase;
  margin-bottom: 2px;
}

.cell-val {
  font-size: 13px;
  font-weight: 900;
  color: #0f172a;
}

.cell-val-status {
  font-size: 13px;
  font-weight: 900;
}

/* Ledger Monolith */
.ledger-monolith {
  border: 1px solid #e2e8f0;
}

.monolith-title {
  font-size: 1.15rem;
  font-weight: 950;
  color: #0f172a;
  line-height: 1.2;
}

.monolith-sub {
  font-size: 11.5px;
  font-weight: 700;
  color: #94a3b8;
}

/* Hub Architecture */
.hub-entry-card {
  border: 1px solid #e2e8f0;
}

.hub-icon-shell {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hub-icon-shell.indigo {
  background: #eef2ff;
  border: 1px solid #e0e7ff;
}

.hub-icon-shell.orange {
  background: #fff7ed;
  border: 1px solid #ffedd5;
}

.hub-title {
  font-size: 15px;
  font-weight: 950;
  color: #1e293b;
  margin-bottom: 1px;
}

.hub-hint {
  font-size: 11px;
  font-weight: 700;
  color: #94a3b8;
}

/* Utils */
.border-bottom {
  border-bottom: 1px solid #f1f5f9;
}

.shadow-soft {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
}

.ga-6 {
  gap: 24px;
}

.ga-4 {
  gap: 16px;
}

@media (max-width: 650px) {

  .prime-avatar-ring,
  .identity-stack {
    display: none !important;
  }

  .panoramic-inner {
    justify-content: center !important;
    padding: 8px !important;
  }

  .intel-matrix {
    width: 100%;
    justify-content: center;
    background: transparent;
    border: none;
  }
}
</style>
