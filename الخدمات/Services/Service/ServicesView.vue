<template>
  <!-- <AttendanceExemptionRequestForm /> -->
  <add-service v-model="drawer" :data="data" :getData="getData" :items="items" />
  <custom-data-table
    :="{
      headers,
      items,
      getData,
      create: () => (drawer = true),
      delItem: API_URLS.SERVICES,
      editItem: handleEdit,
      actionList,
    }"
  >
    <template v-slot:action v-if="$state?.is_super_user">
      <custom-btn
        :label="$t('activateAllServicesForUniversities')"
        class="me-2"
        color="success"
        prepend-icon="mdi-check-all"
        @click="activateAllServices"
      />
    </template>

    <template v-slot:item-slot="{ item, key }">
      <span v-if="key === 'is_active'">
        <v-tooltip
          location="top"
          :text="item.is_active ? $t('deactivate') : $t('activate')"
        >
          <template v-slot:activator="{ props }">
            <v-btn
              v-bind="props"
              variant="outlined"
              size="small"
              :color="item.is_active ? 'success' : 'error'"
              @click="toggleServiceStatus(item.id)"
            >
              <v-icon :icon="item.is_active ? 'mdi-check-circle' : 'mdi-close-circle'" />
            </v-btn>
          </template>
        </v-tooltip>
      </span>
    </template>

    <template v-slot:top>
      <div class="table-hint-container ma-4 pa-3 d-flex align-center rounded-lg">
        <div class="hint-icon-wrapper me-3 d-flex align-center justify-center">
          <v-icon color="primary" size="20">mdi-lightbulb-on-outline</v-icon>
        </div>
        <div class="text-caption text-grey-darken-2 font-weight-medium">
          <span class="text-primary font-weight-bold">تلميح:</span>
          {{ $t("service_status_note") }}
        </div>
      </div>
    </template>
  </custom-data-table>

  <add-service-version
    v-model="dialogs.serviceversions"
    :items="items"
    :data="data"
    :getData="getData"
    :serviceId="selected_service?.id"
  />
  <!-- Dialogs -->
  <service-prerequisites-dialog
    v-model="dialogs.prerequisites"
    :service="selected_service"
  />
  <!-- مراحل سير الخدمة -->
  <service-workflow-dialog v-model="dialogs.workflow" :service="selected_service" />
  <!-- Premium Status Toggle Dialog -->
  <v-dialog
    v-model="dialogs.status"
    max-width="500"
    persistent
    transition="dialog-bottom-transition"
  >
    <v-card class="premium-card overflow-hidden" rounded="xl">
      <div
        :class="[
          'pa-6 text-white d-flex align-center',
          statusState.isActive ? 'header-gradient-error' : 'header-gradient-success',
        ]"
      >
        <v-icon size="32" class="me-4">{{
          statusState.isActive ? "mdi-close-circle-outline" : "mdi-check-circle-outline"
        }}</v-icon>
        <div>
          <div class="text-h6 font-weight-bold">
            {{ statusState.isActive ? "تأكيد تعطيل الخدمة" : "تأكيد تفعيل الخدمة" }}
          </div>
          <div class="text-caption opacity-80">
            {{ statusState.serviceName }}
          </div>
        </div>
      </div>

      <v-card-text class="pa-6 pt-8 text-center">
        <v-icon
          :color="statusState.isActive ? 'error' : 'success'"
          size="64"
          class="mb-4"
        >
          {{
            statusState.isActive ? "mdi-alert-circle-outline" : "mdi-information-outline"
          }}
        </v-icon>
        <div class="text-body-1 font-weight-medium text-grey-darken-2">
          {{
            statusState.isActive
              ? "هل أنت متأكد من رغبتك في تعطيل هذه الخدمة؟"
              : "هل أنت متأكد من رغبتك في تفعيل هذه الخدمة؟"
          }}
        </div>
        <div class="text-caption text-grey mt-2" v-if="statusState.isActive">
          ملاحظة: تعطيل الخدمة سيمنع المستخدمين من الوصول إليها.
        </div>
      </v-card-text>

      <v-divider class="border-opacity-25" />

      <v-card-actions class="pa-6 bg-grey-lighten-5">
        <v-btn
          variant="text"
          color="grey-darken-1"
          class="px-6 font-weight-bold rounded-pill"
          @click="dialogs.status = false"
        >
          إلغاء
        </v-btn>
        <v-spacer />
        <v-btn
          :color="statusState.isActive ? 'error' : 'success'"
          variant="flat"
          class="px-8 font-weight-bold rounded-pill shadow-status"
          :class="statusState.isActive ? 'shadow-error' : 'shadow-success'"
          @click="confirmStatusToggle"
        >
          {{ statusState.isActive ? "تأكيد التعطيل" : "تأكيد التفعيل" }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <custom-dialog
    v-model="dialogs.portal"
    title="ربط مع البوابة"
    width="100%"
    height="100%"
  >
    <PortalTargetMappingView :fk_service="fk_service" />
  </custom-dialog>
</template>

<script>
import PortalTargetMappingView from "./components/PortalTargetMappingView.vue";
/**
 * ServicesView Component
 * Manages the list of services, their status, locking, and configurations.
 */

const API_URLS = {
  SERVICES: "d-services/services/",
  ORG_CONFIG: "d-services/organization-service-config/",
};

export default {
  name: "ServicesView",
  components: { PortalTargetMappingView },

  data() {
    return {
      API_URLS,
      drawer: false,
      data: {},
      items: {},
      selected_service: {},

      dialogs: {
        prerequisites: false,
        serviceversions: false,
        workflow: false,
        installments: false,
        settings: false,
        permissions: false,
        stage_permissions: false,
        status: false,
        portal: false,
      },

      statusState: {
        id: null,
        serviceName: "",
        isActive: false,
      },
    };
  },

  computed: {
    headers() {
      return [
        { title: this.$t("service_name"), key: "name_ar" },
        { title: this.$t("service_name_en"), key: "name_en", show: false },
        { title: this.$t("service_code"), key: "code", show: false },
        { title: this.$t("service_category"), key: "category__display" },
        { title: this.$t("requires_approval"), key: "requires_approval" },
        { title: this.$t("is_repeatable"), key: "is_repeatable" },

        {
          title: this.$t("output_template_type"),
          key: "output_template_type__display",
        },
        {
          title: this.$t("output_data_function"),
          key: "output_data_function",
          show: false,
        },
        {
          title: this.$t("request_form_template"),
          key: "input_template_type__display",
        },
        {
          title: this.$t("input_data_function"),
          key: "input_data_function",
          show: false,
        },
        {
          title: this.$t("target_audience_component"),
          key: "target_audience_component__display",
        },
        {
          title: this.$t("base_audience_component"),
          key: "base_audience_component__display",
          show: false,
        },
        { title: this.$t("is_active"), key: "is_active" },
        {
          title: this.$t("requester_image_function"),
          key: "requester_image_function",
          show: false,
        },

        {
          title: this.$t("icon"),
          key: "icon",
          show: false,
        },
        {
          title: this.$t("description"),
          key: "description",
          show: false,
        },
      ];
    },
  },

  methods: {
    /**
     * Fetch services data
     */
    async getData(params = this.$params) {
      try {
        const response = await this.$axios(API_URLS.SERVICES, params);
        this.items = response.data;
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },

    /**
     * Handle status toggle click
     */
    toggleServiceStatus(id) {
      const service = this.findServiceById(id);
      if (!service) return;

      this.statusState.id = id;
      this.statusState.serviceName = service.name_ar;
      this.statusState.isActive = service.is_active;
      this.dialogs.status = true;
    },

    /**
     * Confirm service active/inactive status toggle
     */
    async confirmStatusToggle() {
      try {
        const res = await this.$axios.patch(
          `${API_URLS.SERVICES}${this.statusState.id}/toggle-active/`
        );
        this.$alert("update", {
          message: res.data?.message || "تم تغيير حالة الخدمة بنجاح",
        });
        this.dialogs.status = false;
        this.getData();
      } catch (error) {
        console.error("Error toggling status:", error);
      }
    },
    /**
     * Activate all services for all universities
     */
    async activateAllServices() {
      try {
        const res = await this.$axios.post(API_URLS.ORG_CONFIG);
        this.$alert("add", {
          message: {
            الرسالة: res.data?.message,
            "تم انشاء": res.data?.created_count,
            "تم تخطي": res.data?.skipped_count,
            "اجمالي المؤسسات": res.data?.total_orgs,
            "اجمالي الخدمات": res.data?.total_services,
          },
        });
      } catch (error) {
        console.error("Error activating all services:", error);
      }
    },

    /**
     * Navigation helper
     */
    navigateToScreen(screen, param, query = {}) {
      this.$navigateTo({
        ar: param?.name_ar,
        name: screen,
        params: param,
        query: query,
        blank: false,
      });
    },

    handleEdit(data) {
      this.data = { ...data };
      this.drawer = true;
    },

    openSettings() {
      this.dialogs.settings = true;
    },

    findServiceById(id) {
      return (
        this.items?.results?.find((s) => s.id === id) ||
        this.items?.find?.((s) => s.id === id)
      );
    },

    actionList(item) {
      const select = (dialog) => {
        this.selected_service = { ...item };
        this.dialogs[dialog] = true;
      };

      return [
        // {
        //   title_ar: "تفاصيل الخدمة",
        //   title_en: "Service Details",
        //   click: () => {
        //     this.navigateToScreen("service-details", {
        //       service_id: item.id,
        //       is_details: true,
        //       name_ar: `${item?.name_ar} / تفاصيل الخدمة`,
        //     });
        //   },
        // },
        {
          title_ar: "اصدارات الخدمة",
          title_en: "Service Versions",
          click: () => select("serviceversions"),
        },
        {
          title_ar: "خطوات سير الخدمة",
          title_en: "Service Steps",
          click: () => select("workflow"),
        },
        {
          title_ar: "متطلبات الخدمة",
          title_en: "Service Prerequisites",
          click: () => select("prerequisites"),
        },
        {
          title_ar: "ربط مع البوابة",
          title_en: "Portal target mapping",
          click: () => {
            this.fk_service = item.id;
            select("portal");
          },
        },
      ];
    },
  },
};
</script>

<style scoped>
.table-hint-container {
  background: linear-gradient(to left, #e3f2fd, #ffffff);
  border: 1px solid #bbdefb;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

.hint-icon-wrapper {
  background-color: #ffffff;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.15);
}

.premium-card {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25) !important;
}

.header-gradient {
  background: linear-gradient(135deg, #fb8c00 0%, #ffb300 100%);
}

.header-gradient-success {
  background: linear-gradient(135deg, #43a047 0%, #66bb6a 100%);
}

.header-gradient-error {
  background: linear-gradient(135deg, #d32f2f 0%, #ef5350 100%);
}

.warning-box {
  background-color: #fff3e0;
  border-right: 4px solid #fb8c00;
}

.info-box {
  background-color: #e8f5e9;
  border-right: 4px solid #43a047;
}

.history-card {
  background-color: #fafafa;
  border: 1px dashed #e0e0e0 !important;
}

.shadow-warning {
  box-shadow: 0 4px 14px 0 rgba(251, 140, 0, 0.39) !important;
}

.shadow-success {
  box-shadow: 0 4px 14px 0 rgba(67, 160, 71, 0.39) !important;
}

.shadow-error {
  box-shadow: 0 4px 14px 0 rgba(211, 47, 47, 0.39) !important;
}

.opacity-80 {
  opacity: 0.8;
}

/* RTL Adjustments */
[dir="rtl"] .warning-box,
[dir="rtl"] .info-box {
  border-right: 4px solid;
  border-left: none;
}
</style>
