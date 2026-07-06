<template>
  <div class="services-catalog">
    <!-- Ultra-Premium Control Header -->
    <header class="catalog-premium-header" :class="{ 'is-scrolled': !isAtTop }">
      <div class="header-upper-layer">
        <div class="h-container">
          <div class="h-brand">
            <v-btn
              icon="mdi-arrow-right"
              variant="tonal"
              class="h-back-pill"
              @click="$router.push({ name: 'services-dashboard' })"
            ></v-btn>
            <div class="h-title-stack">
              <h1 class="h-main-title">دليل الخدمات الرقمية</h1>
              <span class="h-subtitle">استكشف واطلب الخدمات الجامعية بكل سهولة</span>
            </div>
          </div>

          <div class="h-meta">
            <div class="h-status-pill">
              <span class="pulse-dot"></span>
              <span class="status-label"
                ><b>{{ filteredServices.length }}</b> خدمة متاحة حالياً</span
              >
            </div>
          </div>
        </div>
      </div>

      <div class="header-control-layer">
        <div class="h-container">
          <div class="control-wrapper">
            <nav class="category-segmented-control">
              <button
                v-for="cat in categories"
                :key="cat.id"
                class="segment-item"
                :class="{ active: filter.category === cat.id }"
                @click="(filter.category = cat.id), getData()"
              >
                <v-icon size="18" class="me-2">{{ cat.icon || "mdi-folder" }}</v-icon>
                <span>{{ cat.name }}</span>
              </button>
            </nav>

            <div class="control-actions">
              <div class="premium-search-field">
                <v-icon class="search-icon-p">mdi-magnify</v-icon>
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="ابحث عن خدمة محددة..."
                  class="search-input-p"
                />
                <transition name="fade">
                  <v-btn
                    v-if="searchQuery"
                    icon="mdi-close"
                    variant="text"
                    size="x-small"
                    class="search-clear-p"
                    @click="searchQuery = ''"
                  ></v-btn>
                </transition>
              </div>

              <v-btn
                icon="mdi-refresh"
                variant="outlined"
                class="refresh-action-btn"
                @click="resetFilters"
              >
                <v-icon size="18">mdi-refresh</v-icon>
              </v-btn>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content Grid -->
    <main class="catalog-main-content">
      <!-- Loading State -->
      <v-row dense v-if="loading">
        <v-col v-for="n in 8" :key="n" cols="12" md="3" sm="6">
          <v-skeleton-loader type="card" class="rounded-xl"></v-skeleton-loader>
        </v-col>
      </v-row>

      <!-- Services Grid -->
      <transition-group
        name="stagger"
        tag="div"
        class="modern-services-grid"
        v-if="!loading && filteredServices.length"
      >
        <article
          v-for="service in filteredServices"
          :key="service.fk_service.id"
          class="modern-service-card"
          :class="{
            'is-locked': service.is_locked,
            'is-inactive': !service.fk_service.is_active,
          }"
        >
          <!-- Card Header Visual -->
          <div class="m-card-header">
            <div class="m-icon-container">
              <v-icon size="28" color="white">{{
                service.fk_service.icon || "mdi-school"
              }}</v-icon>
              <div class="m-icon-glow"></div>
            </div>

            <div class="m-header-meta">
              <span class="m-service-id">#{{ service.fk_service.code }}</span>
              <div
                class="m-status-badge"
                :class="service.fk_service.is_active ? 'active' : 'inactive'"
              >
                <span class="m-status-dot"></span>
                {{ service.fk_service.is_active ? "نشط" : "معطل" }}
              </div>
            </div>
          </div>

          <!-- Card Body Content -->
          <div class="m-card-body">
            <div class="m-title-area">
              <h3 class="m-service-title">{{ service.fk_service.name_ar }}</h3>
              <p class="m-service-subtitle">{{ service.fk_service.name_en }}</p>
            </div>

            <div class="m-category-chip">
              <v-icon size="14" class="me-1">mdi-tag-outline</v-icon>
              {{ service.fk_service.category__display || service.fk_service.category }}
            </div>

            <p class="m-service-description">
              {{
                service.fk_service.description ||
                "استكشف تفاصيل هذه الخدمة الجامعية وقم بتقديم طلبك الآن بكل سهولة."
              }}
            </p>

            <!-- Feature Tags -->
            <div class="m-feature-tags">
              <div
                class="m-tag"
                :class="{ 'is-priority': service.fk_service.requires_approval }"
              >
                <v-icon size="14">{{
                  service.fk_service.requires_approval
                    ? "mdi-shield-check"
                    : "mdi-lightning-bolt"
                }}</v-icon>
                <span>{{
                  service.fk_service.requires_approval ? "موافقة مطلوبة" : "تنفيذ مباشر"
                }}</span>
              </div>
              <div class="m-tag">
                <v-icon size="14">{{
                  service.fk_service.is_repeatable ? "mdi-repeat" : "mdi-check-circle"
                }}</v-icon>
                <span>{{
                  service.fk_service.is_repeatable ? "خدمة متكررة" : "مرة واحدة"
                }}</span>
              </div>
            </div>
          </div>

          <!-- Card Footer Actions -->
          <div class="m-card-footer">
            <v-tooltip text="تقديم طلب جديد" location="top">
              <template v-slot:activator="{ props }">
                <button
                  v-bind="props"
                  class="m-btn-primary-sm"
                  @click="requestService(service)"
                >
                  <span>طلب الخدمة</span>
                </button>
              </template>
            </v-tooltip>

            <v-tooltip text="طلباتي" location="top">
              <template v-slot:activator="{ props }">
                <button
                  v-bind="props"
                  class="m-btn-action"
                  @click="viewRequests(service)"
                >
                  <v-icon size="18">mdi-clipboard-text-outline</v-icon>
                </button>
              </template>
            </v-tooltip>

            <v-menu location="bottom end" transition="scale-transition" v-if="$state.is_manager">
              <template v-slot:activator="{ props: menuProps }">
                <v-tooltip text="المزيد" location="top">
                  <template v-slot:activator="{ props: tooltipProps }">
                    <button
                      v-bind="{ ...menuProps, ...tooltipProps }"
                      class="m-btn-action"
                    >
                      <v-icon size="18">mdi-dots-vertical</v-icon>

                    </button>
                  </template>
                </v-tooltip>
              </template>
              <div class="m-dropdown-list">
                <div class="m-dropdown-header">
                  <span class="m-dropdown-title">{{ service.fk_service.name_ar }}</span>
                </div>
                <div class="m-dropdown-body">
                  <button
                    v-for="(action, idx) in actionList(service.fk_service)"
                    :key="idx"
                    class="m-dropdown-item"
                    @click="action.click"
                  >
                    <v-icon size="18" class="me-3">{{ action.icon }}</v-icon>
                    <span>{{ action.title_ar }}</span>
                  </button>
                  <div class="m-dropdown-divider"></div>
                  <button
                    class="m-dropdown-item"
                    :class="service.is_locked ? 'text-success' : 'text-warning'"
                    @click="handleLockToggle(service.fk_service.id)"
                  >
                    <v-icon size="18" class="me-3">{{
                      service.is_locked ? "mdi-lock-open-outline" : "mdi-lock-outline"
                    }}</v-icon>
                    <span>{{ service.is_locked ? "فتح الخدمة" : "قفل الخدمة" }}</span>
                  </button>
                </div>
              </div>
            </v-menu>
          </div>

          <!-- Modern Lock Overlay -->
          <div v-if="service.is_locked" class="m-lock-overlay">
            <div class="m-lock-blur"></div>
            <div class="m-lock-content">
              <div class="m-lock-circle">
                <v-icon size="32" color="white">mdi-lock-outline</v-icon>
              </div>
              <h4 class="m-lock-title">الخدمة غير متاحة حالياً</h4>
              <p class="m-lock-desc">يرجى التواصل مع الإدارة للمزيد من التفاصيل</p>
              <button class="m-lock-btn" @click="handleLockToggle(service.fk_service.id)">
                طلب تفعيل
              </button>
            </div>
          </div>
        </article>
      </transition-group>

      <!-- Modern Empty State -->
      <div v-else-if="!loading" class="modern-empty-state">
        <div class="m-empty-visual">
          <div class="m-empty-blob"></div>
          <v-icon size="80" color="primary" class="m-empty-icon"
            >mdi-text-search-variant</v-icon
          >
        </div>
        <h3 class="m-empty-title">لم نجد ما تبحث عنه</h3>
        <p class="m-empty-desc">تأكد من كتابة اسم الخدمة بشكل صحيح أو اختر تصنيفاً آخر</p>
        <button class="m-empty-reset-btn" @click="resetFilters">
          <v-icon size="20" class="me-2">mdi-refresh</v-icon>
          إعادة تعيين الفلاتر
        </button>
      </div>
    </main>

    <!-- Dialogs (Keep existing logic) -->
    <service-workflow-dialog
      v-model="dialogs.workflow"
      :service="selected_service"
    />
    <service-installments-dialog
      v-model="dialogs.installments"
      :service="selected_service"
      @switch-to-first="openSettings"
    />
    <group-service-permission-dialog
      v-model="dialogs.permissions"
      :service="selected_service"
    />
    <stage-permission-dialog
      v-model="dialogs.stage_permissions"
      :service="selected_service"
    />
    <custom-dialog
      v-model="dialogs.settings"
      width="65vw"
      height="auto"
      :title="`${$t('service_setting')} ( ${selected_service?.name_ar} )`"
    >
      <template v-slot>
        <service-settings-dialog
          v-model="dialogs.settings"
          :service="selected_service"
          :embedded="true"
        />
      </template>
    </custom-dialog>
    <!-- اعدادات الـ ERP الاساسية للمنظمة -->
    <custom-dialog
      v-model="dialogs.erp_org_settings"
      width="65vw"
      height="auto"
      :title="`${$t('erp_services_settings')} ( ${selected_service?.name_ar} )`"
    >

      <template v-slot>
        <AddERPSettingsDialog
          v-model="dialogs.erp_org_settings"
          :service="selected_service"
          :embedded="true"
        />
      </template>
    </custom-dialog>
    <!-- اعدادات الـ ERP على مستوى التخصصات -->
    <custom-dialog
      v-model="dialogs.specialization_erp_settings"
      width="auto"
      height="auto"
      :title="`${$t('erp_services_settings')} ( ${selected_service?.name_ar} )`"
    >

      <template v-slot>
        <AddERPSettingsForSpecializationDialog
          v-model="dialogs.specialization_erp_settings"
          :service="selected_service"
          :embedded="true"
        />
      </template>
    </custom-dialog>
    <task-list-for-stages-dialog
      v-model="dialogs.task_list_for_stages"
      :service="selected_service"
    />
    <manage-print-setting-for-workflow-step
      v-model="dialogs.manage_print_setting"
      :service="selected_service"
    />

    <!-- Lock Dialog -->
    <v-dialog v-model="dialogs.lock" max-width="500" persistent>
      <v-card class="m-dialog-card" rounded="xl">
        <div class="m-dialog-header warning">
          <v-icon size="32" color="white">mdi-lock-outline</v-icon>
          <div class="ms-4">
            <div class="text-h6 font-weight-bold text-white">تأكيد قفل الخدمة</div>
            <div class="text-caption text-white opacity-80">
              {{ lockState.serviceName }}
            </div>
          </div>
        </div>
        <v-card-text class="pa-6">
          <div class="m-warning-box mb-6 d-flex align-center pa-4 rounded-lg">
            <v-icon color="warning" size="28" class="me-4">mdi-alert-decagram</v-icon>
            <div class="text-body-2 font-weight-medium text-warning-darken-2">
              تحذير: سيتم إقفال جميع الطلبات الجارية أو التي تحت الانتظار لهذه الخدمة
              فوراً.
            </div>
          </div>
          <v-textarea
            v-model="lockState.reason"
            label="سبب القفل"
            placeholder="يرجى توضيح سبب القفل للإدارة..."
            variant="outlined"
            rows="3"
            auto-grow
            :rules="[(v) => !!v || 'سبب القفل مطلوب']"
            class="mt-4"
          />
        </v-card-text>
        <v-card-actions class="pa-6">
          <v-btn variant="text" @click="dialogs.lock = false">إلغاء</v-btn>
          <v-spacer />
          <v-btn
            color="warning"
            variant="flat"
            :disabled="!lockState.reason"
            @click="confirmLock"
            >تأكيد القفل</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Unlock Dialog -->
    <v-dialog v-model="dialogs.unlock" max-width="500" persistent>
      <v-card class="m-dialog-card" rounded="xl">
        <div class="m-dialog-header success">
          <v-icon size="32" color="white">mdi-lock-open-outline</v-icon>
          <div class="ms-4">
            <div class="text-h6 font-weight-bold text-white">تأكيد فتح الخدمة</div>
            <div class="text-caption text-white opacity-80">
              {{ lockState.serviceName }}
            </div>
          </div>
        </div>
        <v-card-text class="pa-6">
          <div class="m-info-box mb-6 d-flex align-center pa-4 rounded-lg">
            <v-icon color="success" size="28" class="me-4"
              >mdi-information-variant</v-icon
            >
            <div class="text-body-2 font-weight-medium text-success-darken-2">
              ملاحظة: سيتم فتح جميع الطلبات التي تم إقفالها عند قفل الخدمة فقط.
            </div>
          </div>
          <p class="text-center text-body-1 font-weight-bold">
            هل أنت متأكد من رغبتك في إعادة تفعيل هذه الخدمة؟
          </p>
        </v-card-text>
        <v-card-actions class="pa-6">
          <v-btn variant="text" @click="dialogs.unlock = false">إلغاء</v-btn>
          <v-spacer />
          <v-btn color="success" variant="flat" @click="confirmUnlock">تأكيد الفتح</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
const API_URLS = {
  SERVICES: "d-services/services/",
  ORG_CONFIG: "d-services/organization-service-config/",
};

export default {
  name: "ServicesCatalogView",
  data() {
    return {
      API_URLS,
      searchQuery: "",
      filter: {
        category: null,
      },
      categories: [],
      services: [],
      services__fk_service: [],
      selected_service: {},
      dialogs: {
        prerequisites: false,
        workflow: false,
        installments: false,
        settings: false,
        permissions: false,
        stage_permissions: false,
        task_list_for_stages: false,
        lock: false,
        unlock: false,
        status: false,
      },
      lockState: {
        id: null,
        serviceName: "",
        reason: "",
        prevReason: "",
        prevDate: "",
      },
      loading: false,
      url: "d-services/organization-service-config/?fk_org=",
      url_request_service: "d-services/requests/",
      isAtTop: true,
    };
  },
  mounted() {
    window.addEventListener("scroll", this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener("scroll", this.handleScroll);
  },
  async created() {
    await this.getData();
    try {
      const cats = await this.$dataList()?.ServiceCategoryChoice?.method();
      if (cats && cats.length > 0) {
        this.categories = cats;
      }
    } catch (e) {
      console.error("Error fetching categories:", e);
    }

    if (!this.categories.find((c) => c.id === 0)) {
      this.categories.unshift({ id: 0, name: "الكل", icon: "mdi-view-grid" });
    }
    this.filter.category = 0;
  },
  computed: {
    filteredServices() {
      if (!this.services) return [];
      let result = this.services;

      if (this.searchQuery.trim()) {
        const q = this.searchQuery.toLowerCase().trim();
        result = result.filter((s) => {
          const nameAr = (s.fk_service?.name_ar || "").toLowerCase();
          const nameEn = (s.fk_service?.name_en || "").toLowerCase();
          const code = (s.fk_service?.code || "").toLowerCase();
          const category = (s.fk_service?.category || "").toLowerCase();

          return (
            nameAr.includes(q) ||
            nameEn.includes(q) ||
            code.includes(q) ||
            category.includes(q)
          );
        });
      }

      return result;
    },
  },
  watch: {
    // "filter.category"(newVal) {
    //   this.getData();
    // },
  },
  methods: {
    handleScroll() {
      this.isAtTop = window.scrollY < 50;
    },
    async getData() {
      this.loading = true;
      try {
        const response = await this.$axios(this.url + this.$state.organization_id, {
          params: {
            category: this.filter.category ? this.filter.category : undefined,
          },
        });
        this.services = response?.data.data ?? [];
        this.services__fk_service = this.services?.map((s) => s.fk_service);
      } catch (error) {
        console.error("Error fetching services:", error);
        this.services = [];
        this.services__fk_service = [];
      } finally {
        this.loading = false;
      }
    },
    resetFilters() {
      this.searchQuery = "";
      this.filter.category = null;
      this.getData();
    },
    moveToNex(screen, params = null, query = null) {
      this.$navigateTo({
        name: screen,
        params: params,
        query: query,
        blank: false,
      });
    },
    requestService(service) {
      if (service.is_locked) return;
      this.moveToNex("request-service", {
        fk_service: service.fk_service.id,
      });
    },
    viewRequests(service) {
      this.moveToNex("service-requests", {
        fk_service: service.fk_service.id,
      });
    },
    actionList(item) {
      const select = (dialog) => {
        console.log(item);
        this.selected_service = { ...item };
        this.dialogs[dialog] = true;
      };
      return [
        {
          title_ar: "اعدادات الخدمة",
          title_en: "Service Settings",
          icon: "mdi-cog-outline",
          click: () => select("settings"),
        },
        {
          title_ar: "اعدادات الـ ERP",
          title_en: "ERP Settings",
          icon: "mdi-cog-outline",
          click: () => select("erp_org_settings"),
        },
        {
          title_ar: "اعدادات الـ ERP للتخصص",
          title_en: "ERP Settings for Specialization",
          icon: "mdi-cog-outline",
          click: () => select("specialization_erp_settings"),
        },

        {
          title_ar: "خطة الأقساط",
          title_en: "Installments Plan",
          icon: "mdi-calendar-clock-outline",
          click: () => select("installments"),
        },
        {
          title_ar: "صلاحيات الخدمة",
          title_en: "Service Permissions",
          icon: "mdi-shield-account-outline",
          click: () => select("permissions"),
        },
        {
          title_ar: "صلاحيات المرحلة",
          title_en: "Stage Permissions",
          icon: "mdi-shield-check-outline",
          click: () => select("stage_permissions"),
        },
        {
          title_ar: "قائمة المهام للمراحل",
          title_en: "Stage Permissions",
          icon: "mdi-shield-check-outline",
          click: () => select("task_list_for_stages"),
        },

        {
          title_ar: "ادارة اعدادات الطباعة لخطوات سير العمل",
          title_en: "Manage Print Setting For Workflow Step",
          icon: "mdi-printer-settings",
          click: () => select("manage_print_setting"),
        },
      ];
    },
    handleLockToggle(id) {
      const service = this.findServiceById(id);
      if (!service) return;

      this.lockState.id = id;
      this.lockState.serviceName = service.fk_service.name_ar;

      if (service.is_locked) {
        this.lockState.prevReason = service.locked_reason || "";
        this.lockState.prevDate = service.locked_at || "";
        this.dialogs.unlock = true;
      } else {
        this.lockState.reason = "";
        this.dialogs.lock = true;
      }
    },
    findServiceById(id) {
      return this.services?.find((s) => s.fk_service.id === id);
    },
    async confirmLock() {
      try {
        const res = await this.$axios.patch(
          `${API_URLS.ORG_CONFIG}${this.lockState.id}/toggle-lock/`,
          { locked_reason: this.lockState.reason }
        );
        this.$alert("update", {
          message: res.data?.message || "تم قفل الخدمة بنجاح",
        });
        this.dialogs.lock = false;
        this.getData();
      } catch (error) {
        console.error("Error locking service:", error);
      }
    },
    async confirmUnlock() {
      try {
        const res = await this.$axios.patch(
          `${API_URLS.ORG_CONFIG}${this.lockState.id}/toggle-lock/`
        );
        this.$alert("update", {
          message: res.data?.message || "تم فتح الخدمة بنجاح",
        });
        this.dialogs.unlock = false;
        this.getData();
      } catch (error) {
        console.error("Error unlocking service:", error);
      }
    },
    openSettings() {
      this.dialogs.installments = false;
      setTimeout(() => {
        this.dialogs.settings = true;
      }, 300);
    },
  },
};
</script>

<style scoped>
.catalog-premium-header {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.catalog-premium-header.is-scrolled {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
}

.h-container {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 60px;
}

/* Upper Layer */
.header-upper-layer {
  padding: 24px 0;
  border-bottom: 1px solid #f1f5f9;
}

.header-upper-layer .h-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.h-brand {
  display: flex;
  align-items: center;
  gap: 20px;
}

.h-back-pill {
  width: 44px !important;
  height: 44px !important;
  border-radius: 14px !important;
  background: #f8fafc !important;
  color: #64748b !important;
  border: 1px solid #e2e8f0 !important;
}

.h-title-stack {
  display: flex;
  flex-direction: column;
}

.h-main-title {
  font-size: 1.6rem;
  font-weight: 900;
  color: #0f172a;
  margin: 0;
  letter-spacing: -0.5px;
}

.h-subtitle {
  font-size: 0.85rem;
  color: #94a3b8;
  font-weight: 600;
  margin-top: 2px;
}

.h-status-pill {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px;
  background: #f0f9ff;
  border: 1px solid #e0f2fe;
  border-radius: 100px;
  font-size: 0.85rem;
  color: #0369a1;
  font-weight: 700;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background: #0ea5e9;
  border-radius: 50%;
  position: relative;
}

.pulse-dot::after {
  content: "";
  position: absolute;
  inset: -4px;
  background: #0ea5e9;
  border-radius: 50%;
  opacity: 0.4;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.4;
  }
  100% {
    transform: scale(2.5);
    opacity: 0;
  }
}

/* Control Layer */
.header-control-layer {
  background: #f8fafc;
  padding: 12px 0;
}

.control-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 40px;
}

/* Segmented Control */
.category-segmented-control {
  display: flex;
  background: #f1f5f9;
  padding: 4px;
  border-radius: 14px;
  gap: 2px;
}

.segment-item {
  display: flex;
  align-items: center;
  padding: 8px 20px;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 700;
  color: #64748b;
  white-space: nowrap;
}

.segment-item:hover {
  color: #0f172a;
}

.segment-item.active {
  background: white;
  color: #3b82f6;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* Premium Search */
.control-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.premium-search-field {
  position: relative;
  width: 360px;
}

.search-icon-p {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  pointer-events: none;
  transition: all 0.3s;
}

.search-input-p {
  width: 100%;
  padding: 10px 44px 10px 40px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  color: #1e293b;
}

.search-input-p:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.08);
}

.search-input-p:focus + .search-icon-p {
  color: #3b82f6;
}

.search-clear-p {
  position: absolute;
  left: 6px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8 !important;
}

.refresh-action-btn {
  width: 44px !important;
  height: 44px !important;
  border-radius: 12px !important;
  border-color: #e2e8f0 !important;
  color: #64748b !important;
  background: white !important;
}

.refresh-action-btn:hover {
  background: #f1f5f9 !important;
  color: #0f172a !important;
  border-color: #cbd5e1 !important;
}

/* Main Content Grid */
.catalog-main-content {
  max-width: 1600px;
  margin: 0 auto;
  padding: 40px 60px;
}

.modern-services-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 32px;
}

/* Modern Service Card */
.modern-service-card {
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.modern-service-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px -8px rgba(0, 0, 0, 0.08);
  border-color: #cbd5e1;
}

/* Card Header */
.m-card-header {
  padding: 20px 20px 0;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.m-icon-container {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  background: linear-gradient(135deg, #334155 0%, #1e293b 100%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 16px -4px rgba(15, 23, 42, 0.2);
}

.modern-service-card:hover .m-icon-container {
  background: #0f172a;
  transform: translateY(-2px) rotate(-4deg);
  box-shadow: 0 12px 24px -8px rgba(15, 23, 42, 0.4);
}

.m-icon-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    circle at center,
    rgba(255, 255, 255, 0.1) 0%,
    transparent 70%
  );
  opacity: 0;
  transition: opacity 0.4s;
}

.modern-service-card:hover .m-icon-glow {
  opacity: 1;
}

.m-header-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
}

.m-service-id {
  font-size: 0.7rem;
  font-weight: 800;
  color: #94a3b8;
  background: #f8fafc;
  padding: 3px 8px;
  border-radius: 6px;
  border: 1px solid #f1f5f9;
}

.m-status-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.7rem;
  font-weight: 800;
  padding: 3px 10px;
  border-radius: 100px;
}

.m-status-badge.active {
  background: #ecfdf5;
  color: #059669;
}
.m-status-badge.inactive {
  background: #fef2f2;
  color: #dc2626;
}

.m-status-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: currentColor;
}

/* Card Body */
.m-card-body {
  padding: 16px 20px;
  flex: 1;
}

.m-service-title {
  font-size: 1.1rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 2px;
  line-height: 1.4;
}

.m-service-subtitle {
  font-size: 0.8rem;
  color: #64748b;
  margin: 0 0 12px;
  font-weight: 500;
}

.m-category-chip {
  display: inline-flex;
  align-items: center;
  padding: 5px 10px;
  background: #f1f5f9;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 700;
  color: #475569;
  margin-bottom: 12px;
}

.m-service-description {
  font-size: 0.85rem;
  color: #64748b;
  line-height: 1.6;
  margin: 0 0 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 2.7rem;
}

.m-feature-tags {
  display: flex;
  gap: 8px;
}

.m-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 10px;
  background: #f8fafc;
  border-radius: 8px;
  font-size: 0.7rem;
  font-weight: 700;
  color: #64748b;
  border: 1px solid #f1f5f9;
}

.m-tag.is-priority {
  background: #eff6ff;
  color: #2563eb;
  border-color: #dbeafe;
}

/* Card Footer */
.m-card-footer {
  padding: 12px 20px 20px;
  display: flex;
  gap: 8px;
  align-items: center;
}

.m-btn-primary-sm {
  flex: 1;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0f172a;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.2s;
}

.m-btn-primary-sm:hover {
  background: #2563eb;
}

.m-btn-action {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.m-btn-action:hover {
  background: #e2e8f0;
  color: #0f172a;
}

/* Modern Lock Overlay */
.m-lock-overlay {
  position: absolute;
  inset: 0;
  z-index: 20;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(10px);
}

.modern-service-card.is-locked:hover .m-lock-overlay {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.modern-service-card.is-locked .m-card-header,
.modern-service-card.is-locked .m-card-body,
.modern-service-card.is-locked .m-card-footer {
  filter: grayscale(0.5) opacity(0.8);
  transition: all 0.4s ease;
}

.modern-service-card.is-locked:hover .m-card-header,
.modern-service-card.is-locked:hover .m-card-body,
.modern-service-card.is-locked:hover .m-card-footer {
  filter: grayscale(1) blur(4px) opacity(0.4);
}

.m-lock-blur {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.7);
  /* backdrop-filter: blur(8px); */
}

.m-lock-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
}

.m-lock-circle {
  width: 72px;
  height: 72px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.m-lock-title {
  font-size: 1.25rem;
  font-weight: 900;
  margin-bottom: 8px;
}

.m-lock-desc {
  font-size: 0.9rem;
  opacity: 0.7;
  margin-bottom: 24px;
}

.m-lock-btn {
  padding: 12px 32px;
  background: white;
  color: #0f172a;
  border: none;
  border-radius: 14px;
  font-size: 0.95rem;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s;
}

.m-lock-btn:hover {
  background: #f8fafc;
  transform: scale(1.05);
}

/* Dropdown Menu */
.m-dropdown-list {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  border: 1px solid #f1f5f9;
  min-width: 260px;
  overflow: hidden;
}

.m-dropdown-header {
  padding: 16px 20px;
  background: #f8fafc;
  border-bottom: 1px solid #f1f5f9;
}

.m-dropdown-title {
  font-size: 0.9rem;
  font-weight: 800;
  color: #1e293b;
}

.m-dropdown-body {
  padding: 8px;
}

.m-dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #475569;
  transition: all 0.2s;
  text-align: right;
}

.m-dropdown-item:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.m-dropdown-divider {
  height: 1px;
  background: #f1f5f9;
  margin: 8px 16px;
}

/* Dialog Info Boxes */
.m-warning-box {
  background: #fff7ed;
  border: 1px solid #ffedd5;
}

.text-warning-darken-2 {
  color: #9a3412;
}

.m-info-box {
  background: #f0fdf4;
  border: 1px solid #dcfce7;
}

.text-success-darken-2 {
  color: #166534;
}

/* Empty State */
.modern-empty-state {
  text-align: center;
  padding: 100px 40px;
}

.m-empty-visual {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 0 auto 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.m-empty-blob {
  position: absolute;
  width: 100%;
  height: 100%;
  background: #eff6ff;
  border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%;
}

@keyframes blobAnim {
  0% {
    border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%;
  }
  33% {
    border-radius: 60% 40% 30% 70% / 50% 60% 40% 60%;
  }
  66% {
    border-radius: 30% 70% 60% 40% / 60% 40% 50% 40%;
  }
  100% {
    border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%;
  }
}

.m-empty-title {
  font-size: 1.75rem;
  font-weight: 900;
  color: #0f172a;
  margin-bottom: 12px;
}

.m-empty-desc {
  font-size: 1.1rem;
  color: #64748b;
  margin-bottom: 32px;
}

.m-empty-reset-btn {
  display: inline-flex;
  align-items: center;
  padding: 14px 32px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 16px;
  font-size: 1rem;
  font-weight: 800;
  box-shadow: 0 10px 20px -5px rgba(59, 130, 246, 0.4);
  cursor: pointer;
  transition: all 0.3s;
}

.m-empty-reset-btn:hover {
  background: #2563eb;
  transform: translateY(-2px);
}

/* Animations */
.stagger-enter-active {
  transition: all 0.5s ease;
}
.stagger-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

/* Responsive Refinements */
@media (max-width: 1400px) {
  .h-container {
    padding: 0 40px;
  }
  .modern-services-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
  }
}

@media (max-width: 1200px) {
  .modern-services-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1100px) {
  .h-container {
    padding: 0 24px;
  }
  .control-wrapper {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }
  .premium-search-field {
    width: 100%;
  }
  .search-input-p:focus {
    width: 100%;
  }

  .category-segmented-control {
    overflow-x: auto;
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none; /* IE 10+ */
    padding: 6px;
  }

  .category-segmented-control::-webkit-scrollbar {
    display: none; /* Chrome, Safari, Opera */
  }

  .segment-item {
    padding: 8px 16px;
    flex-shrink: 0;
  }
}

@media (max-width: 768px) {
  .header-upper-layer {
    padding: 16px 0;
  }
  .header-upper-layer .h-container {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .h-brand {
    width: 100%;
  }
  .h-meta {
    width: 100%;
  }
  .h-status-pill {
    width: 100%;
    justify-content: center;
  }

  .h-main-title {
    font-size: 1.3rem;
  }
  .h-subtitle {
    font-size: 0.8rem;
  }

  .catalog-main-content {
    padding: 20px;
  }
  .modern-services-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .m-card-header {
    padding: 16px 16px 0;
  }
  .m-card-body {
    padding: 12px 16px;
  }
  .m-card-footer {
    padding: 12px 16px 16px;
  }

  .m-service-title {
    font-size: 1rem;
  }
  .m-lock-title {
    font-size: 1.1rem;
  }
  .m-lock-desc {
    font-size: 0.8rem;
  }

  .m-empty-visual {
    width: 140px;
    height: 140px;
  }
  .m-empty-title {
    font-size: 1.4rem;
  }
}

@media (max-width: 480px) {
  .h-container {
    padding: 0 16px;
  }
  .h-brand {
    gap: 12px;
  }
  .h-back-pill {
    width: 38px !important;
    height: 38px !important;
    border-radius: 10px !important;
  }

  .control-actions {
    gap: 10px;
  }
  .refresh-action-btn {
    width: 40px !important;
    height: 40px !important;
  }

  .m-feature-tags {
    flex-wrap: wrap;
  }
  .m-tag {
    font-size: 0.65rem;
    padding: 4px 8px;
  }

  .m-btn-primary-sm {
    font-size: 0.8rem;
  }
}
</style>
