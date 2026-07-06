<template>
  <div class="ma-4">
    <!-- Header: Details -->
    <v-card class="mb-4" rounded="lg" elevation="2">
      <v-card-text>
        <div class="d-flex align-center mb-4">
          <v-avatar
            color="primary"
            variant="tonal"
            rounded="lg"
            size="x-large"
            class="me-4"
          >
            <v-icon size="32">mdi-information</v-icon>
          </v-avatar>
          <div>
            <div class="text-h5 font-weight-bold">{{ service?.name_ar }}</div>
            <div class="text-subtitle-1 text-medium-emphasis">
              {{ service?.name_en }}
            </div>
          </div>
        </div>

        <v-row>
          <v-col cols="12" md="3" sm="6">
            <div class="d-flex align-center">
              <v-icon color="grey" class="me-2">mdi-barcode</v-icon>
              <div>
                <div class="text-caption text-medium-emphasis">
                  {{ $t("service_code") }}
                </div>
                <div class="font-weight-bold">{{ service?.code || "-" }}</div>
              </div>
            </div>
          </v-col>
          <v-col cols="12" md="3" sm="6">
            <div class="d-flex align-center">
              <v-icon color="grey" class="me-2">mdi-shape</v-icon>
              <div>
                <div class="text-caption text-medium-emphasis">
                  {{ $t("service_category") }}
                </div>
                <div class="font-weight-bold">
                  {{ service?.category__display || "-" }}
                </div>
              </div>
            </div>
          </v-col>
          <v-col cols="12" md="3" sm="6">
            <div class="d-flex align-center">
              <v-icon
                :color="service?.is_active ? 'success' : 'error'"
                class="me-2"
              >
                {{
                  service?.is_active ? "mdi-check-circle" : "mdi-close-circle"
                }}
              </v-icon>
              <div>
                <div class="text-caption text-medium-emphasis">
                  {{ $t("status") }}
                </div>
                <div class="font-weight-bold">
                  {{ service?.is_active ? $t("active") : $t("inactive") }}
                </div>
              </div>
            </div>
          </v-col>
          <v-col cols="12" md="3" sm="6">
            <div class="d-flex align-center">
              <v-icon color="grey" class="me-2">mdi-file-document-check</v-icon>
              <div>
                <div class="text-caption text-medium-emphasis">
                  {{ $t("requires_approval") }}
                </div>
                <div class="font-weight-bold">
                  {{ service?.requires_approval ? $t("yes") : $t("no") }}
                </div>
              </div>
            </div>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Tabs -->
    <v-card rounded="lg" elevation="2">
      <v-tabs v-model="tab" color="primary" align-tabs="start">
        <v-tab value="workflow">
          <v-icon start>mdi-sitemap</v-icon>
          {{ $t("addServiceWorkflow") }}
        </v-tab>
        <v-tab value="prerequisites">
          <v-icon start>mdi-format-list-checks</v-icon>
          {{ $t("addServicePrerequisite") }}
        </v-tab>
        <v-tab value="installments">
          <v-icon start>mdi-cash-multiple</v-icon>
          {{ $t("serviceInstallmentsPlan") }}
        </v-tab>
        <v-tab value="settings">
          <v-icon start>mdi-cog</v-icon>
          {{ $t("serviceSettings") }}
        </v-tab>
      </v-tabs>

      <v-card-text>
        <v-window v-model="tab">
          <v-window-item value="workflow">
            <service-workflow-dialog
              v-model="dialogs.workflow"
              :service="service"
              :embedded="true"
              :is_details="true"
            />
          </v-window-item>

          <v-window-item value="prerequisites">
            <service-prerequisites-dialog
              v-model="dialogs.prerequisites"
              :service="service"
              :embedded="true"
               :is_details="true"
            />
          </v-window-item>

          <v-window-item value="installments">
            <service-installments-dialog
              v-model="dialogs.installments"
              :service="service"
              :embedded="true"
               :is_details="true"
            />
          </v-window-item>

          <v-window-item value="settings">
            <service-settings-dialog
              v-model="dialogs.settings"
              :service="service"
              :embedded="true"
               :is_details="true"
            />
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import ServiceWorkflowDialog from "./components/ServiceWorkflowDialog.vue";
import ServicePrerequisitesDialog from "./components/ServicePrerequisitesDialog.vue";
import ServiceInstallmentsDialog from "./components/ServiceInstallmentsDialog.vue";
import ServiceSettingsDialog from "./components/ServiceSettingsDialog.vue";

export default {
  components: {
    ServiceWorkflowDialog,
    ServicePrerequisitesDialog,
    ServiceInstallmentsDialog,
    ServiceSettingsDialog,
  },
  data() {
    return {
      tab: null,
      service_id: null,
      is_details: null,
      service: {},
      dialogs: {
        workflow: false,
        prerequisites: false,
        installments: false,
        settings: false,
      },
    };
  },
  created() {
    this.is_details = this.$route.params.is_details;
    this.service_id =
      this.$route.params.id ||
      this.$route.params.service_id ||
      this.$route.query.service_id;
    if (this.service_id) {
      this.getServiceDetails();
    }
  },
  methods: {
    async getServiceDetails() {
      // Fetch service details. Assuming we can fetch by ID from the main list URL or a specific detail URL.
      // Since ServicesView uses "d-services/services/", we'll use that + ID.
      try {
        const response = await this.$axios.get(
          `d-services/services/${this.service_id}/`
        );
        this.service = response.data;
      } catch (error) {
        console.error("Error fetching service details", error);
        this.$snack("error", { message: "فشل تحميل بيانات الخدمة" });
      }
    },
  },
};
</script>
