<template>
  <div class="order-management-dashboard px-4">
    <v-row class="main-layout-grid">
      <!-- Main Content Area (8/12) - Second on Mobile, First on Desktop -->
      <v-col cols="12" lg="8" class="pa-2 order-2 order-lg-1">
        <div class="sections-container d-flex flex-column gap-6">

          <!-- Modern Section Header: Service Details -->
          <section class="premium-glass-card">
            <div class="section-header-pro">
              <div class="d-flex align-center flex-wrap gap-3">
                <div class="accent-line"></div>
                <div class="d-flex align-center">
                  <div class="icon-orb bg-gradient-blue ml-4">
                    <v-icon icon="mdi-file-document-edit-outline" color="white" size="20"></v-icon>
                  </div>
                </div>
                <div>
                  <h3 class="text-h6 font-weight-black text-slate-900 mb-0">بيانات الخدمة المطلوبة</h3>
                  <p class="text-caption text-slate-400 font-weight-bold mb-0">كافة التفاصيل الفنية والخيارات المختارة
                  </p>
                </div>
              </div>
            </div>
            <div class="pa-4 pa-md-6">
              <v-skeleton-loader v-if="loading?.main" type="article" class="bg-transparent"></v-skeleton-loader>
              <InfoGrid v-else :items="data.main_data_cards" />
            </div>
          </section>

          <!-- Modern Section Header: Target Audience -->
          <section class="premium-glass-card">
            <div class="section-header-pro">
              <div class="d-flex align-center flex-wrap gap-3">
                <div class="accent-line indigo"></div>
                <div class="d-flex align-center">
                  <div class="icon-orb bg-gradient-indigo ml-4">
                    <v-icon icon="mdi-account-group-outline" color="white" size="20"></v-icon>
                  </div>
                </div>
                <div>
                  <h3 class="text-h6 font-weight-black text-slate-900 mb-0">بيانات المستهدف بالخدمة</h3>
                  <p class="text-caption text-slate-400 font-weight-bold mb-0">معلومات الفئة المستفيدة وحالتها
                    الأكاديمية</p>
                </div>
              </div>
            </div>
            <div class="pa-4 pa-md-6">
              <div class="audience-hero-banner mb-6">
                <div class="d-flex align-center flex-wrap gap-3">
                  <v-avatar color="white" size="48" class="elevation-1 ml-4 hidden-xs">
                    <v-icon icon="mdi-bullseye-arrow" color="primary" size="24"></v-icon>
                  </v-avatar>
                  <div class="flex-grow-1 min-w-0">
                    <span class="text-tiny text-primary-dark font-weight-black d-block mb-1">الفئة الرسمية</span>
                    <h4 class="text-subtitle-1 font-weight-black text-slate-800 line-height-1 text-truncate">
                      {{ requestDetails?.target_audience_schema?.label_ar || '---' }}
                    </h4>
                  </div>
                  <v-chip color="primary" size="small" variant="flat"
                    class="font-weight-black rounded-pill mt-2 mt-sm-0">نشط</v-chip>
                </div>
              </div>
              <InfoGrid v-if="!loading?.target" :items="data.target_data_cards" />
              <v-skeleton-loader v-else type="list-item-two-line" class="bg-transparent"></v-skeleton-loader>
            </div>
          </section>

          <!-- Modern Section Header: Order Metadata -->
          <section class="premium-glass-card">
            <div class="section-header-pro">
              <div class="d-flex align-center flex-wrap gap-3">
                <div class="accent-line slate"></div>
                <div class="d-flex align-center">
                  <div class="icon-orb bg-gradient-slate ml-4">
                    <v-icon icon="mdi-information-variant" color="white" size="20"></v-icon>
                  </div>
                </div>
                <div>
                  <h3 class="text-h6 font-weight-black text-slate-900 mb-0">بيانات الطلب النظامية</h3>
                  <p class="text-caption text-slate-400 font-weight-bold mb-0">الأرقام المرجعية، التواريخ، وحالة الدفع
                  </p>
                </div>
              </div>
            </div>
            <div class="pa-4 pa-md-6">
              <InfoGrid :items="data.order_details" :translate="true" />
            </div>
          </section>

        </div>
      </v-col>

      <!-- Sidebar Area (4/12) - First on Mobile, Second on Desktop -->
      <v-col cols="12" lg="4" class="pa-2 order-1 order-lg-2">
        <aside class="sidebar-sticky-wrapper d-flex flex-column gap-6">

          <!-- Floating Requester Card -->
          <div class="profile-card-wrapper">
            <!-- <div class="card-title-mini mb-3">صاحب الطلب</div> -->
            <ProfileCard type="user" :title="requestDetails?.requester_name || '---'"
              :subtitle="requestDetails?.requester_description || '---'"
              :image="requestDetails?.requester_image ? (setting?.url?.slice(0, -1) + requestDetails?.requester_image) : ''"
              :infoValue="requestDetails?.requester_email || '---'" infoIcon="mdi-email-outline"
              avatarColor="primary" />
          </div>

          <!-- Vertical Timeline/Notes Card -->
          <OrderNotes />
        </aside>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import InfoGrid from "./sub-components/OrderBasicInfo/InfoGrid.vue";
import OrderNotes from "./sub-components/OrderBasicInfo/OrderNotes.vue";
import ProfileCard from "./sub-components/OrderBasicInfo/ProfileCard.vue";

export default {
  name: "OrderBasicInfo",
  components: {
    InfoGrid,
    OrderNotes,
    ProfileCard,
  },
  inject: ["context"],
  props: {
    requestDetails: {
      type: Object,
      default: () => { },
      required: true,
    },
    includedKeys: {
      type: Array,
      default: () => [
        "request_number",
        "version_name",
        "fk_service__code",
        "fk_service__name",
        "payment_status__display",
        "request_source__display",
        "requested_at",
        "start_request_at",
      ],
    },
  },
  emits: ["add-note", "edit"],
  data() {
    return {
      data: {},
      loading: {},
      url: "d-services/service-requests/",
      request_id: this.$route.params?.request_id,
    };
  },
  async created() {
    await this.initCards();
    await this.orderDetailsOnly();
  },
  methods: {
    async initCards() {
      try {
        this.loading.target = true;
        this.loading.main = true;
        if (
          this.requestDetails?.target_audience_schema &&
          !this.data?.target_data_cards?.length
        ) {
          this.data.target_data_cards = await this.formatViewData({
            schema: this.requestDetails?.target_audience_schema,
            data: this.requestDetails?.target_audience_data,
          });
          this.loading.target = false;
        }
        if (
          this.requestDetails?.version_schema &&
          !this.data?.main_data_cards?.length
        ) {
          this.data.main_data_cards = await this.formatViewData({
            schema: this.requestDetails?.version_schema,
            data: this.requestDetails?.version_data,
          });
          this.loading.main = false;
        }
      } catch (error) {
        console.log(error);
      } finally {
        this.loading = {};
      }
    },

    orderDetailsOnly() {
      const filtered = {};
      for (const key of this.includedKeys) {
        if (this.requestDetails) {
          filtered[key] = this.requestDetails[key];
        }
      }
      this.data.order_details = filtered;
    },
    async formatViewData(service_schema) {
      var formatted_data = {};
      if (service_schema?.schema?.fields?.length) {
        for (const field of service_schema?.schema?.fields) {
          if (field?.name_list) {
            const { label, method, title, value } = this.$dataList(
              service_schema.schema?.attrs[field?.name]
                ? service_schema.schema?.attrs[field?.name]?.param
                : false
            )[field?.name_list];

            formatted_data[field?.label_ar || this.$t(label)] =
              service_schema?.data[`${field?.name}_name`];
          } else {
            formatted_data[field?.label_ar] = service_schema?.data[field?.name];
          }
        }
      }

      return formatted_data;
    },
  },
  watch: {
    requestDetails(newVal) {
      this.initCards();
      this.orderDetailsOnly();
    },
  },
};
</script>

<style scoped>

.order-management-dashboard {
  background-color: #f8fafc;
  min-height: 100vh;
  font-family: 'Almarai', sans-serif !important;
}

.premium-glass-card {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  position: relative;
}

/* .premium-glass-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px -10px rgba(0, 0, 0, 0.06);
  border-color: #e2e8f0;
} */

.section-header-pro {
  padding: 20px 28px;
  position: relative;
  background: #ffffff;
  border-bottom: 1px solid #f1f5f9;
}

.accent-line {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 5px;
  background: #3b82f6;
  border-radius: 4px 0 0 4px;
}

.accent-line.indigo {
  background: #6366f1;
}

.accent-line.slate {
  background: #94a3b8;
}

.icon-orb {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
}

.icon-orb::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, transparent 100%);
}

.bg-gradient-blue {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
}

.bg-gradient-indigo {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
}

.bg-gradient-slate {
  background: linear-gradient(135deg, #94a3b8, #64748b);
}

.audience-hero-banner {
  background: linear-gradient(135deg, #f8fafc 0%, #eff6ff 100%);
  border-radius: 16px;
  padding: 20px;
  border: 1px solid #e2e8f0;
  position: relative;
  overflow: hidden;
}

.audience-hero-banner::after {
  content: '';
  position: absolute;
  top: -20px;
  left: -20px;
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, rgba(37, 99, 235, 0.05) 0%, transparent 70%);
}

.sidebar-sticky-wrapper {
  position: sticky;
  top: 24px;
}

.card-title-mini {
  font-size: 11px;
  font-weight: 800;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  padding-right: 4px;
}

.gap-6 {
  gap: 24px;
}

@media (max-width: 1264px) {
  .sidebar-sticky-wrapper {
    position: static;
    margin-top: 32px;
  }
}

.text-tiny {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.text-slate-900 {
  color: #0f172a !important;
}

.text-slate-800 {
  color: #1e293b !important;
}

.text-slate-400 {
  color: #94a3b8 !important;
}

.text-primary-dark {
  color: #1d4ed8 !important;
}

.line-height-1 {
  line-height: 1.4;
}
</style>
