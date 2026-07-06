<template>
  <div class="order-detail-master-layout ma-n2 ">
    <div class="main-scroll-area pb-32">
      <!-- Sticky Header Group -->
      <div class="sticky-header-group">
        <div class="header-surface">
          <OrderHeader
            :request-id="request_details?.request_number"
            :title="request_details?.fk_service__name_ar"
            :subtitle="request_details?.fk_service__name_en"
            :date="request_details?.requested_at"
            :priority="request_details?.priority__display"
            :status="request_details?.status"
            :statusLoading="loading['request']"
            @lock="openDialog('lock-order')"
          />

          <!-- Navigation Tabs -->
          <div class="tabs-wrapper mt-2">
            <div class="pa-0">
              <v-tabs
                v-model="activeTab"
                height="56"
                class="pro-tabs-container"
                hide-slider
                selected-class="tab-selected"
              >
                <v-tab
                  v-for="tab in navigationTabs?.filter((t) => !t?.hide)"
                  :key="tab.value"
                  :value="tab.value"
                  class="pro-tab-item"
                  :ripple="false"
                >
                  <div class="tab-content-wrapper">
                    <v-icon
                      :icon="tab.icon"
                      size="20"
                      class="tab-icon"
                    ></v-icon>
                    <span class="tab-label">{{ tab.label }}</span>
                    <span
                      v-if="tab.count"
                      class="tab-badge"
                      :class="{ 'active-badge': activeTab === tab.value }"
                    >
                      {{ tab.count }}
                    </span>
                  </div>
                </v-tab>
              </v-tabs>
            </div>
          </div>
        </div>
      </div>

      <!-- Content Area -->
      <div class="container-fluid bg-slate-50 pb-16 pt-6">
        <v-window v-model="activeTab" class="overflow-visible" touch="false">
          <!-- Basic Info -->
          <v-window-item value="basic">
            <OrderBasicInfo
              v-if="activeTab === 'basic'"
              :request-details="request_details"
              @add-note="openDialog('add-note')"
            />
          </v-window-item>

          <!-- Form View -->
          <v-window-item value="form">
            <OrderOutputsInput
              v-if="activeTab === 'form'"
              :type="'input'"
              :url="url"
            />
          </v-window-item>

          <!-- Financial -->
          <v-window-item value="financial">

            <OrderFinancialInfo
              v-if="activeTab === 'financial'"
              ref="financialInfoRef"
              :financials="financialData"
              :installments="request_details?.installments"
              :grant-data="grantData"
              :discount-data="discountData"
              @pay="handlePayment"
              @add-installment="openDialog('add-installment')"
              @edit-installment="(item) => openDialog('edit-installment', item)"
              @delete-installment="
                (item) => openDialog('delete-installment', item)
              "
              @grant-updated="handleGrantUpdate"
              @discount-updated="handleDiscountUpdate"
            />
          </v-window-item>
          <!-- Stages -->
          <v-window-item v-if="viewStagesTab" value="stages" class="h-100">
            <OrderStages
              v-if="activeTab === 'stages'"
              :stages="request_details?.action_steps"
              @action="handleStageAction"
            />
          </v-window-item>

          <!-- Attachments -->
          <v-window-item value="attachments">
            <OrderAttachments
              v-if="activeTab === 'attachments'"
              :files="request_details?.attachments"
              @add="openDialog('add-attachment')"
              @view="handleFilePreview"
              @edit="(file) => openDialog('edit-attachment', file)"
              @download="handleFileDownload"
              @delete="(file) => openDialog('delete-attachment', file)"
            />
          </v-window-item>

          <!-- Outputs View -->
          <v-window-item value="outputs">
            <OrderOutputsInput
              v-if="activeTab === 'outputs'"
              :type="'output'"
              :url="url"
            />
          </v-window-item>

          <!-- Logs -->
          <v-window-item value="logs">
            <!-- <OrderLogs
              :logs="logs"
              @filter="handleLogFilter"
              @view-all="handleLogViewAll"
              @add-note="(log) => openDialog('add-log-note', log)"
            /> -->
            <service-records v-if="activeTab === 'logs'" />
          </v-window-item>
        </v-window>
      </div>
    </div>

    <!-- Footer Actions -->
    <div id="request_details">
      <OrderFooterActions @extra="handleExtraAction" @print="printRequest" />
    </div>

    <!-- Shared Dialogs & Notifications -->
    <BaseDialog
      v-model="dialog.show"
      v-bind="dialog"
      @confirm="handleDialogConfirm"
    >
    </BaseDialog>
    <BaseNotification v-model="notification.show" v-bind="notification" />
  </div>
</template>

<script>
import OrderHeader from "@/pages/Services/ServiceRequest/components/OrderHeader";
import OrderBasicInfo from "@/pages/Services/ServiceRequest/components/OrderBasicInfo";
import OrderFinancialInfo from "@/pages/Services/ServiceRequest/components/OrderFinancialInfo";
import OrderStages from "@/pages/Services/ServiceRequest/components/OrderStages";
import OrderAttachments from "@/pages/Services/ServiceRequest/components/OrderAttachments";
import OrderOutputsInput from "@/pages/Services/ServiceRequest/components/sub-components/OrderOutputsInput/OrderOutputsInput";
import ServiceRecords from "@/pages/Services/ServiceRequest/ServiceRecords/ServiceRecords";
import OrderFooterActions from "@/pages/Services/ServiceRequest/components/OrderFooterActions";
export default {
  components: {
    OrderHeader,
    OrderBasicInfo,
    OrderFinancialInfo,
    OrderStages,
    OrderAttachments,
    OrderOutputsInput,
    ServiceRecords,
    OrderFooterActions,
  },
  data() {
    return {
      // url_context: this.context.url_context,
      // request_id: this.context.request_id,
      request_id: this.$route?.params?.request_id,

      request_details: {},
      input_data: {},
      output_data: {},
      loading: {},

      available_actions: [],
      url: "d-services/service-requests/",
      url_actions_status: "d-services/request-actions-status/",
      activeTab: "basic",
      dialog: {
        show: false,
        title: "",
        subtitle: "",
        type: "primary",
        mode: "form",
        confirmText: "حفظ",
        loading: false,
        data: {},
        fields: [],
        icon: "",
        confirmMessage: "",
        confirmSubMessage: "",
      },
      notification: {
        show: false,
        message: "",
        description: "",
        type: "success",
      },
      footerConfig: {},
    };
  },
  provide() {
    return {
      context: this,
      request_id: this.request_details?.id,
      getRequestDetails: this.getRequestDetails,
      checkActionPermission: this.checkActionPermission,
    };
  },
  async created() {
    if (this.request_id) {
      await this.getRequestDetails();
      await this.getRequestInputData();
      await this.getRequestOutputData();
      // await this.fetchOrderDetails();
    }
  },
  computed: {
    viewStagesTab() {
      return !!this.request_details?.action_steps?.length;
    },
    navigationTabs() {
      return [
        {
          label: "معلومات الطلب",
          value: "basic",
          icon: "mdi-information-outline",
        },
        {
          label: "الاستمارة",
          value: "form",
          icon: "mdi-form-select",
          hide: !this.request_details?.input_template_type,
        },
        { label: "البيانات المالية", value: "financial", icon: "mdi-finance" },
        {
          label: "سير العمل",
          value: "stages",
          icon: "mdi-ray-start-arrow",
          hide: !this.viewStagesTab,
        },
        {
          label: "المرفقات",
          value: "attachments",
          icon: "mdi-paperclip",
          count: this.request_details?.attachments?.length,
        },
        {
          label: "المخرجات",
          value: "outputs",
          icon: "mdi-file-certificate-outline",
          hide: !this.request_details?.output_template_type,
        },
        { label: "سجل النشاط", value: "logs", icon: "mdi-history" },
      ];
    },
    financialData() {
      return {
        total: this.request_details?.total_fee ?? 0.0,
        paid: this.request_details?.amount_paid ?? 0.0,
        remaining: this.request_details?.remaining_amount ?? 0.0,
        payment_status: this.request_details?.payment_status,
      };
    },
  },
  // mounted() {
  //   this.fetchOrderDetails();
  // },
  methods: {
    async getRequestDetails() {
      this.loading["request"] = true;
      try {
        const response = await this.$axios(`${this.url}${this.request_id}/`);
        this.request_details = response.data?.data ?? {};
        await this.getActionsStatus();
      } catch (e) {
        console.log(e);
      } finally {
        this.loading["request"] = false;
      }
    },
    async getRequestInputData() {
      return await this.$axios(
        `${this.url}${this.request_id}/input-data/`
      ).then((res) => {
        this.input_data = res.data.data?.input_data ?? {};
      });
    },
    async getRequestOutputData() {
      return await this.$axios(
        `${this.url}${this.request_id}/output-data/`
      ).then((res) => {
        this.output_data = res.data.data?.output_data ?? {};
      });
    },
    async getActionsStatus() {
      await this.$axios(`${this.url_actions_status}${this.request_id}/`).then(
        (res) => {
          this.available_actions = res.data?.data?.available_actions ?? [];
        }
      );
    },

    checkActionPermission(action) {
      return (
        this.available_actions?.some(
          (action_perm) =>
            action_perm.action === action && action_perm.has_permission == true
        ) || false
      );
    },

    showNotification(msg, desc, type = "success") {
      this.notification.message = msg;
      this.notification.description = desc;
      this.notification.type = type;
      this.notification.show = true;
    },
    openDialog(type, item = null) {
      this.dialog.show = true;
      this.dialog.data = item ? { ...item } : {};

      // Reset defaults
      this.dialog.loading = false;
      this.dialog.mode = "form";

      switch (type) {
        case "return-order":
          this.dialog.title = "إعادة للمراجعة";
          this.dialog.subtitle = "إعادة الطلب للمستفيد لتعديل الملاحظات";
          this.dialog.confirmText = "إرسال للمراجعة";
          this.dialog.type = "warning";
          this.dialog.icon = "mdi-keyboard-return";
          this.dialog.fields = [
            {
              key: "notes",
              label: "ملاحظات التعديل المطلوبة",
              type: "textarea",
            },
          ];
          break;

        case "lock-order":
          this.dialog.title = "قفل الطلب";
          this.dialog.mode = "form";
          this.dialog.action = "lock";
          this.dialog.confirmMessage = "هل أنت متأكد من قفل الطلب؟";
          this.dialog.confirmSubMessage =
            "لن يتمكن المستفيد من إجراء أي تعديلات إضافية";
          this.dialog.confirmText = "قفل الطلب";
          this.dialog.type = "error";
          this.dialog.icon = "mdi-lock-alert";
          this.dialog.fields = [
            {
              key: "locked_reason",
              label: "ملاحظة سبب اقفال الطلب",
              type: "textarea",
            },
          ];
          break;

        case "approve-stage":
          this.dialog.title = "اعتماد المرحلة";
          this.dialog.subtitle = `اعتماد مرحلة "${
            item?.name || "المرحلة الحالية"
          }" والانتقال للمرحلة التالية`;
          this.dialog.confirmText = "اعتماد وإرسال";
          this.dialog.type = "success";
          this.dialog.icon = "mdi-check-decagram";
          this.dialog.fields = [
            {
              key: "note",
              label: "ملاحظات الاعتماد (اختياري)",
              type: "textarea",
            },
          ];
          break;

        case "return-stage":
          this.dialog.title = "إرجاع للتعديل";
          this.dialog.subtitle = "إعادة الطلب للمستفيد لاستكمال المتطلبات";
          this.dialog.confirmText = "إرجاع للتعديل";
          this.dialog.type = "warning";
          this.dialog.icon = "mdi-keyboard-return";
          this.dialog.fields = [
            {
              key: "notes",
              label: "ملاحظات التعديل المطلوبة",
              type: "textarea",
            },
          ];
          break;

        case "reject-stage":
          this.dialog.title = "رفض الطلب نهائياً";
          this.dialog.subtitle = "سيتم إغلاق الطلب وإشعار المستفيد";
          this.dialog.confirmText = "تأكيد الرفض";
          this.dialog.type = "error";
          this.dialog.icon = "mdi-close-circle";
          this.dialog.fields = [
            { key: "reason", label: "سبب الرفض (مطلوب)", type: "textarea" },
          ];
          break;

        default:
          this.dialog.title = "إجراء جديد";
          this.dialog.confirmText = "حفظ";
          this.dialog.type = "primary";
          this.dialog.fields = [
            { key: "note", label: "ملاحظات", type: "textarea" },
          ];
      }
    },
    async handleDialogConfirm() {
      const { valid } = await this.$refs.dialogForm.validate();
      if (valid) {
        this.dialog.loading = true;
        setTimeout(() => {
          // Execute stage transitions based on dialog type
          const dialogType = this.dialog.title;
          const dialogData = this.dialog?.data ?? {};
          const action = this.dialog?.action;

          if (action && action == "lock") {
            this.lockRequest(dialogData);
          } else if (
            dialogType === "إرجاع للتعديل" ||
            dialogType === "إعادة للمراجعة"
          ) {
            this.returnToApplicant();
            this.showNotification(
              "تم الإرجاع",
              "تم إرجاع الطلب للمستفيد لاستكمال المتطلبات",
              "warning"
            );
          } else {
            this.showNotification(
              "تمت العملية",
              "تم حفظ التغييرات بنجاح في النظام"
            );
          }

          this.dialog.show = false;
          this.dialog.loading = false;
        }, 1000);
      }
    },
    // handleCopyJson() {
    //   navigator.clipboard.writeText(JSON.stringify(this.mockJsonData, null, 2));
    //   this.showNotification("تم النسخ", "تم نسخ بيانات JSON للحافظة", "info");
    // },
    handlePayment(item) {
      this.showNotification("جاري الدفع", `بدء سداد ${item.type}`, "info");
    },

    handleStageAction({ type, stage }) {
      switch (type) {
        case "approve":
          this.openDialog("approve-stage", stage);
          break;
        case "return":
          this.openDialog("return-stage", stage);
          break;
        case "reject":
          this.openDialog("reject-stage", stage);
          break;
        default:
          this.showNotification("تم الإجراء", `تم تنفيذ ${type} بنجاح`);
      }
    },

    handleExtraAction(action) {
      if (action === "return") {
        this.openDialog("return-order");
      } else {
        this.showNotification("إجراء إضافي", `جاري تنفيذ ${action}`);
      }
    },
    handleFilePreview(file) {
      this.showNotification("معاينة", `فتح ${file.name}`, "info");
    },
    handleFileDownload(file) {
      this.showNotification("تحميل", `بدء تحميل ${file.name}`);
    },
    handleLogFilter() {
      this.showNotification("تصفية", "فتح خيارات التصفية", "info");
    },
    handleLogViewAll() {
      this.showNotification("السجل", "تحميل السجل الكامل", "info");
    },
    handleStageChange(stage) {
      console.log("Stage:", stage.name);
    },
    handleGrantUpdate(data) {
      if (this.grantData) {
        Object.assign(this.grantData, data);
      } else {
        this.grantData = data;
      }
    },
    handleDiscountUpdate(data) {
      if (this.discountData) {
        Object.assign(this.discountData, data);
      } else {
        this.discountData = data;
      }
    },

    // الطباعة
    printRequest() {
      this.$shared.printReport("request_details");
    },
  },
};
</script>

<style>
.order-detail-master-layout {
  background: #f8fafc;
  min-height: 100vh;
}

.sticky-header-group {
  position: sticky;
  top: 0;
  z-index: 99;
  background: transparent;
}

.header-surface {
  background: rgba(255, 255, 255, 0.9);
  /* backdrop-filter: blur(12px); */
  border-bottom: 1px solid rgba(226, 232, 240, 0.8);
  box-shadow: 0 4px 20px -4px rgba(0, 0, 0, 0.05);
}

.tabs-wrapper {
  padding: 0 24px;
}

.pro-tabs-container {
  background: transparent !important;
}

.pro-tab-item {
  text-transform: none !important;
  letter-spacing: 0 !important;
  font-weight: 600 !important;
  font-family: "Almarai", sans-serif !important;
  color: #64748b !important;
  min-width: auto !important;
  padding: 0 8px !important;
  margin-right: 8px;
  border-radius: 12px !important;
}

.tab-content-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 12px;
  transition: all 0.2s;
}

.pro-tab-item:hover .tab-content-wrapper {
  background: #f1f5f9;
  color: #334155;
}

.tab-selected {
  color: #2563eb !important;
}

.tab-selected .tab-content-wrapper {
  background: #eff6ff;
  box-shadow: 0 1px 2px rgba(37, 99, 235, 0.05);
}

.tab-icon {
  opacity: 0.7;
  transition: all 0.2s;
}

.tab-selected .tab-icon {
  opacity: 1;
  transform: scale(1.1);
}

.tab-label {
  font-size: 14px;
}

.tab-badge {
  background: #e2e8f0;
  color: #64748b;
  font-size: 11px;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 6px;
  min-width: 20px;
  text-align: center;
  transition: all 0.2s;
}

.active-badge {
  background: #dbeafe;
  color: #2563eb;
}

@media (max-width: 960px) {
  .tabs-wrapper {
    padding: 0 16px;
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(255, 255, 255, 0.95);
    /* backdrop-filter: blur(12px); */
    border-bottom: 1px solid rgba(226, 232, 240, 0.8);
    margin-top: 0 !important;
  }

  .sticky-header-group {
    position: static !important;
  }

  .header-surface {
    background: #fff;
    border-bottom: none;
    box-shadow: none;
  }
}
</style>
