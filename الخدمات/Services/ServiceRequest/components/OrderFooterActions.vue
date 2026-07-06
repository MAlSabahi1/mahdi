<template>

  <v-footer app class="footer-root pa-0">
    <div class="footer-surface w-100">
      <div  class="py-2 px-3 py-md-4 px-md-8">
        <div class="footer-flex-container">
          <!-- Mobile: "More Actions" Menu Trigger -->
          <div class="d-md-none">
            <v-menu location="top start" :close-on-content-click="false">
              <template v-slot:activator="{ props }">
                <button class="icon-btn more-btn" v-bind="props">
                  <v-icon icon="mdi-dots-vertical" size="24"></v-icon>
                </button>
              </template>

              <v-list class="mobile-actions-list elevation-4 rounded-lg mb-2">
                <!-- Dynamic Extra Actions -->
                <v-list-item v-for="action in extraActions" :key="action.type" @click="action.function(action.type)"
                  link>
                  <template v-slot:prepend>
                    <v-icon :icon="action.icon" :color="action.color" size="20"></v-icon>
                  </template>
                  <v-list-item-title class="text-caption font-weight-bold">{{ action.label }}</v-list-item-title>
                </v-list-item>

                <v-divider v-if="extraActions.length > 0" class="my-1"></v-divider>

                <!-- Secondary Workflow Actions -->
                <v-list-item v-if="checkActionPermission('CANCEL')" @click="openDialog('cancel-order')" link>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-cancel" color="slate-500" size="20"></v-icon>
                  </template>
                  <v-list-item-title class="text-caption font-weight-bold text-slate-500">الغاء
                    الطلب</v-list-item-title>
                </v-list-item>

                <v-list-item v-if="checkActionPermission('REJECT')" @click="openDialog('reject-order')" link>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-close-circle-outline" color="error" size="20"></v-icon>
                  </template>
                  <v-list-item-title class="text-caption font-weight-bold text-error">رفض الطلب</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </div>

          <!-- Desktop: Inline Secondary Actions -->
          <div class="secondary-actions-wrapper d-none d-md-flex">
            <!-- Dynamic Extra Actions Group -->
            <div class="actions-group">
              <v-tooltip v-for="action in extraActions" :key="action.type" :text="action.label" location="top">
                <template v-slot:activator="{ props }">
                  <button class="icon-btn" v-bind="props" @click="action.function(action.type)">
                    <v-icon :icon="action.icon" size="20" :color="action.color"></v-icon>
                  </button>
                </template>
              </v-tooltip>
            </div>

            <div v-if="extraActions.length > 0" class="vertical-sep mx-2"></div>

            <!-- Secondary Workflow Actions -->
            <div class="actions-group">
              <!-- Cancel -->
              <button v-if="checkActionPermission('CANCEL')" class="text-btn" @click="openDialog('cancel-order')">
                الغاء
              </button>

              <!-- Reject -->
              <button v-if="checkActionPermission('REJECT')" class="tonal-btn error"
                @click="openDialog('reject-order')">
                <v-icon icon="mdi-close-circle-outline" size="20"></v-icon>
                <span>رفض الطلب</span>
              </button>
            </div>
          </div>

          <!-- Right: Primary Actions (Always Visible) -->
          <div class="primary-actions-wrapper">

            <!-- Approve -->
            <button v-if="checkActionPermission('START')" class="solid-btn primary"
              @click="openDialog('approve-order')">
              <v-icon icon="mdi-check-decagram" size="20"></v-icon>
              <span>اعتماد الطلب</span>
            </button>

            <v-alert v-else-if="
              requestDetails?.grant_status == 'pending' ||
              requestDetails?.discount_status == 'pending'
            " class="px-0" color="warning" variant="text" density="compact">
              <template #prepend>
                <v-icon end> mdi-alert </v-icon>
              </template>
              يرجى اعتماد او الغاء المنحة او الخصم
            </v-alert>

            <!-- Complete -->
            <button v-if="checkActionPermission('COMPLETE')" class="solid-btn success"
              @click="openDialog('complete-order')">
              <v-icon icon="mdi-check-all" size="20"></v-icon>
              <span>إكمال الطلب</span>
            </button>

          </div>
        </div>
      </div>
    </div>
  </v-footer>

  <!-- Dialogs (Kept as is) -->
  <BaseDialog v-model="dialog.assign_dia" :loading="loading?.grant" icon="account-plus" title="تعيين منحة"
    @confirm="saveGrant()">
    <template #fields>

      <auto-list
        v-model="dialog.grant_party"
        name="GrantSource"
        :rules="[$required]"
        :objects="availableGrantSources"
        @update:modelValue="grantType!=='domestic'?clearInternalDonor(dialog):null"
      ></auto-list>
      <auto-list
        v-if="grantType=='domestic'"
        v-model="dialog.erp_product_for_internal_donors_id"
        name="Schoolarships"
        @update:modelValue="dialog.erp_product_for_internal_donors_name=getNameByID(schoolarships,dialog.erp_product_for_internal_donors_id)"
        :rules="[$required]"
      >
      </auto-list>
      <custom-text-field
        v-model="dialog.grant_percentage"
        icon="percent"
        label="نسبة المنحة"
        type="number"
        :replace_append_icon="requestDetails?.currency__data?.name_ar"
        :rules="[$required, $max_value(100), $min_value(0)]"
      />
    </template>
  </BaseDialog>
  <BaseDialog v-model="dialog.discount_dia" :loading="loading?.discount" @confirm="saveDiscount()" title="اضافة خصم"
    icon="tag-minus" type="warning">

    <template #fields>

      <auto-list
        v-model="dialog.erp_product_for_discount_id"
        name="Discounts"
        @update:modelValue="dialog.erp_product_for_discount_name=getNameByID(discounts,dialog.erp_product_for_discount_id)"
        :rules="[$required]"
      >
      </auto-list>
      <custom-text-field
        v-model="dialog.discount_percentage"
        label="نسبة الخصم"
        type="number"
        append-icon="percent"
        :rules="[
          $required,
          $max_value(100),
          $min_value(1),
        ]"
      />

      <custom-text-note v-model="dialog.discount_reason" icon="note" label="سبب الخصم"
        :rules="[$required, $max_length(250)]" />
    </template>
  </BaseDialog>

  <BaseDialog v-model="dialog.show" @confirm="dialog.procedure" :fields="dialog.fields" :data="dialog.data"
    :title="dialog.title" :type="dialog.type" :icon="dialog.icon" :loading="dialog.isLoading">
  </BaseDialog>
  <BaseNotification v-model="notification.show" v-bind="notification" />
</template>

<script>
export default {
  name: "OrderFooterActions",
  props: {
    // primaryAction: {
    //   type: Object,
    //   default: () => ({
    //     type: "complete",
    //     label: "إكمال الإجراء النهائي",
    //     icon: "mdi-check-all",
    //     color: "primary",
    //   }),
    // },
    // secondaryAction: {
    //   type: Object,
    //   default: null,
    // },
  },
  emits: ["extra", "cancel", "complete"],
  inject: ["context", "getRequestDetails", "checkActionPermission"],
  data() {
    return {
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
        isLoading: false,
      },
      schoolarships:[],
      discounts:[],
      grant_sources:[],

      notification: {},
      loading: {},
      request_details: this.context?.request_details ?? {},
      url: this.context?.url,
      url_grant: "d-services/service-requests/id/assign-grant/",
      url_discount: "d-services/service-requests/id/add-discount/",
      request_id: this.context?.request_id,
    };
  },
  async created(){
    // await this.getRequestDetails()
    // this.request_details = this.context?.request_details ?? {}

    if(this.$dataList && this.$dataList().GrantSource){
      this.grant_sources = await this.$dataList().GrantSource.method();
    }

    if (this.$dataList && this.$dataList().Schoolarships) {
      this.schoolarships =
        await this.$dataList().Schoolarships.method();
    }
    if (this.$dataList && this.$dataList().Discounts) {
      this.discounts =
        await this.$dataList().Discounts.method();
    }
  },
  computed: {
    requestDetails() {
      return this.context?.request_details;
    },
    availableGrantSources(){
      return this.grant_sources?.filter(item=>this.requestDetails?.available_grant_sources_ids?.includes(item?.id))
    },
    grantType(){
      const grant_record = this.availableGrantSources?.find(grant=>grant.id==this.dialog?.grant_party)
      return grant_record?.source_type
    },
    extraActions() {
      return [
        {
          type: "assign",
          label: "تعيين منحة",
          icon: "mdi-account-plus",
          color: "indigo-darken-1",
          show: this.checkActionPermission("ASSIGN_GRANT"),
          function: this.openGrantDialog,
        },
        {
          type: "discount",
          label: "إضافة خصم",
          icon: "mdi-tag-minus",
          color: "amber-darken-3",
          show: this.checkActionPermission("ADD_DISCOUNT"),
          function: this.openDiscountDialog,
        },
      ]?.filter((a) => a?.show);
    },
  },
  methods: {
    getNameByID(data_list,selected_id){
      const record = data_list?.find(item=>item.id==selected_id);
      return record ? record?.name : null
    },
    clearInternalDonor(dialog){
      dialog.erp_product_for_internal_donors_id = null;
      dialog.erp_product_for_internal_donors_name = null;
    },
    openDiscountDialog(dia){
      this.dialog = {};
      this.dialog[`${dia}_dia`] = true;
      this.dialog.erp_product_for_discount_id = this.requestDetails?.erp_product_for_discount_id
      this.dialog.erp_product_for_discount_name = this.requestDetails?.erp_product_for_discount_name

    },
    openGrantDialog(dia) {
      this.dialog = {};
      this.dialog[`${dia}_dia`] = true;
      this.dialog.erp_product_for_internal_donors_id = this.requestDetails?.erp_product_for_internal_donors_id
      this.dialog.erp_product_for_internal_donors_name = this.requestDetails?.erp_product_for_internal_donors_name
      // this.saveGrant();
    },

    openDialog(type, item = null) {
      this.dialog.show = true;
      this.dialog.data = item ? { ...item } : {};

      // Reset defaults
      this.dialog.loading = false;
      this.dialog.mode = "form";

      switch (type) {
        case "approve-order":
          this.dialog.title = "اعتماد الطلب";
          this.dialog.subtitle = "هل أنت متأكد من رغبتك في اعتماد هذا الطلب؟";
          this.dialog.confirmText = "اعتماد نهائي";
          this.dialog.type = "primary";
          this.dialog.action = "approve";
          this.dialog.icon = "check-decagram";
          this.dialog.procedure = this.approveRequest;
          this.dialog.fields = [
            {
              name: "note",
              type: "TextField",
              null: false,
              label_ar: "ملاحظات الاعتماد (اختياري)",
              max_length: 255,
              default: null,
              min_length: null,
              icon: "text-long",

              rows: 6,
            },
          ];
          break;
        case "complete-order":
          this.dialog.title = "انهاء الطلب";
          this.dialog.subtitle = "هل أنت متأكد من رغبتك في اعتماد هذا الطلب؟";
          this.dialog.confirmText = "اعتماد نهائي";
          this.dialog.type = "success";
          this.dialog.action = "complete";
          this.dialog.icon = "check-decagram";
          this.dialog.procedure = this.completeRequest;
          this.dialog.fields = [
            {
              name: "note",
              type: "TextField",
              null: false,
              label_ar: "ملاحظات اكمال الطلب ",
              max_length: 255,
              rows: 5,
              default: null,
              min_length: null,
              icon: "text-long",

              rows: 6,
            },
          ];
          break;
        case "reject-order":
          this.dialog.title = "رفض الطلب";
          this.dialog.subtitle = "يرجى توضيح سبب الرفض لاتخاذ الإجراء";
          this.dialog.confirmText = "تأكيد الرفض";
          this.dialog.type = "error";
          this.dialog.action = "reject";
          this.dialog.icon = "close-octagon-outline";
          this.dialog.procedure = this.rejectRequest;
          this.dialog.fields = [
            {
              name: "reject_reason",
              type: "TextField",
              null: false,
              label_ar: "سبب الرفض (مطلوب)",
              max_length: 255,
              default: null,
              min_length: null,
              icon: "text-long",

              rows: 6,
            },
          ];
          break;
        case "cancel-order":
          this.dialog.title = "الغاء الطلب";
          this.dialog.subtitle = "يرجى توضيح سبب الغاء الطلب لاتخاذ الإجراء";
          this.dialog.confirmText = "تأكيد الالغاء";
          this.dialog.action = "cancel";
          this.dialog.type = "warning";
          this.dialog.icon = "play-circle-outline";
          this.dialog.procedure = this.cancelRequest;
          this.dialog.fields = [
            {
              name: "cancel_reason",
              type: "TextField",
              null: false,
              label_ar: "سبب الالغاء (مطلوب)",
              max_length: 255,
              default: null,
              min_length: null,
              icon: "text-long",

              rows: 6,
            },
          ];
          break;
      }
    },
    async approveRequest() {
      this.dialog.isLoading = true;
      try {
        await this.$axios
          ?.post(
            `${this.url}${this.request_id}/start/`,
            this.dialog?.data ?? {}
          )
          .then((res) => {
            this.getRequestDetails();
            this.showNotification(
              "تم الاعتماد",
              "تم اعتماد المرحلة والانتقال للمرحلة التالية بنجاح",
              "success"
            );
          });
      } catch (error) {
        this.$alert("errorData", {
          icon: this.dialog.icon,
          message: error.response?.data?.error ?? "حدث خطأ ما.",
        });
      } finally {
        this.dialog.isLoading = false;
        this.dialog = {};
      }
    },
    async completeRequest() {
      this.dialog.isLoading = true;
      try {
        await this.$axios
          .post(
            `${this.url}${this.request_id}/complete/`,
            this.dialog?.data ?? {}
          )
          .then((res) => {
            this.getRequestDetails();
            this.showNotification(
              "تم إكمال الطلب",
              "تم إكمال الطلب بنجاح",
              "success"
            );
          });
      } catch (error) {
        this.$alert("errorData", {
          message:
            error.response?.data?.error ??
            "  حدث خطأ ما في عملية اكمال الطلب..",
          sub_message: error.response?.data?.hint,
        });
      } finally {
        this.dialog.isLoading = false;

        this.dialog = {};
      }
    },
    async cancelRequest(data) {
      this.dialog.isLoading = true;
      try {
        await this.$axios
          .post(
            `${this.url}${this.request_id}/cancel/`,
            this.dialog?.data ?? {}
          )
          .then((res) => {
            this.dialog.show = false;
            this.showNotification(
              "تم الغاء الطلب ",
              "تم الالغاء بنجاح وسيتم تحويلك الى قائمة الطلبات ",
              "success"
            );
            setTimeout(() => {
              this.$router.push({ name: "service-requests" });
            }, 3000);
          });
      } catch (error) {
        this.$alert("errorData", {
          message:
            error.response?.data?.error ??
            "  حدث خطأ ما في عملية الغاء الطلب..",
          sub_message: error.response?.data?.hint,
        });
      } finally {
        this.dialog.isLoading = false;
      }
    },
    async rejectRequest(data) {
      this.dialog.isLoading = true;
      try {
        await this.$axios
          .post(
            `${this.url}${this.request_id}/reject/`,
            this.dialog?.data ?? {}
          )
          .then((res) => {
            this.showNotification(
              "تم الرفض",
              "تم رفض الطلب وإغلاقه نهائياً",
              "error"
            );
            setTimeout(() => {
              this.$router.push({
                name: "service-requests",
                fk_service: this.request_details?.fk_service,
              });
            }, 1500);
          });
      } catch (error) {
        const error_data = error.response?.data ?? {};
        const error_message = [];
        error_message.push(error_data?.error);
        error_message.push(error_data?.hint);
        this.$alert("errorData", { message: error_message });
      } finally {
        this.dialog.isLoading = false;
      }
    },

    async saveGrant() {
      try {
        this.loading.grant = true;
        await this.$axios
          ?.post(`${this.url_grant}`?.replace("id", this.requestDetails?.id), {
            fk_grant_source: this.dialog?.grant_party,
            grant_percentage: this.dialog?.grant_percentage,
          })
          .then((res) => {
            this.getRequestDetails();
            this.showNotification(
              "تم الاضافة",
              "تم اضافة منحة للطالب",
              "success"
            );
          });
      } catch (error) {
        this.$alert("errorData", {
          message: error.response.data?.error,
          sub_message: error.response.data?.hint,
        });
      } finally {
        this.loading.grant = false;
        this.dialog = {};
      }
    },
    async saveDiscount() {
      try {
        this.loading.discount = true;
        await this.$axios
          ?.post(
            `${this.url_discount}`?.replace("id", this.requestDetails?.id),
            this.dialog
          )
          .then((res) => {
            this.getRequestDetails();
            this.showNotification(
              "تم الاضافة",
              "تم اضافة خصم للطالب",
              "success"
            );
            this.dialog.discount_dia = false;
          });
      } finally {
        this.loading.discount = false;
        this.dialog = {};
      }
    },

    printRequest() {
      this.$emit("print");
    },
    showNotification(msg, desc, type = "success") {
      this.notification.message = msg;
      this.notification.description = desc;
      this.notification.type = type;
      this.notification.show = true;
    },
  },
};
</script>

<style scoped>

.footer-root {
  font-family: 'Almarai', sans-serif !important;
  z-index: 100 !important;
}

.footer-surface {
  background: #ffffff;
  border-top: 1px solid #e2e8f0;
  box-shadow: 0 -4px 6px -1px rgba(0, 0, 0, 0.05);
}

.footer-flex-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

/* --- Secondary & Extra Actions (Desktop) --- */
.secondary-actions-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.actions-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Icon Buttons */
.icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  border: 1px solid #f1f5f9;
  background: #f8fafc;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s;
}

.icon-btn:hover {
  background: #f1f5f9;
  border-color: #e2e8f0;
  color: #1e293b;
}

.more-btn {
  background: #fff;
  border-color: #e2e8f0;
}

/* Desktop Text Buttons */
.text-btn {
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 700;
  color: #64748b;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: color 0.2s;
}

.text-btn:hover {
  color: #1e293b;
  background: #f8fafc;
}

.tonal-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.tonal-btn.error {
  background: #fef2f2;
  color: #ef4444;
}

.tonal-btn.error:hover {
  background: #fee2e2;
}

/* --- Primary Actions (Right) --- */
.primary-actions-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  /* Take remaining space on mobile */
  justify-content: flex-end;
}

/* Solid Button (Approve/Complete) */
.solid-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 0 24px;
  height: 44px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 700;
  color: #fff;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
  white-space: nowrap;
}

.solid-btn.primary {
  background: #2563eb;
}

.solid-btn.success {
  background: #10b981;
}

.vertical-sep {
  width: 1px;
  height: 24px;
  background: #e2e8f0;
}

.mobile-actions-list {
  min-width: 200px;
  font-family: 'Almarai', sans-serif !important;
}

.text-slate-500 {
  color: #64748b !important;
}

.text-error {
  color: #ef4444 !important;
}

@media (max-width: 960px) {
  .footer-flex-container {
    gap: 12px;
  }

  .solid-btn {
    flex: 1;
    /* Full width on mobile relative to wrapper */
    padding: 0 16px;
    font-size: 14px;
  }

  .primary-actions-wrapper {
    width: 100%;
  }
}
</style>
