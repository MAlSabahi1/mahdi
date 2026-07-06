<template>
  <div class="services-dashboard">
    <!-- Hero Header -->
    <header class="dashboard-hero mb-10">
      <div class="hero-content">
        <div class="d-flex align-center ga-6">
          <div class="hero-icon-wrapper">
            <v-icon size="48" color="white">mdi-view-dashboard-outline</v-icon>
          </div>
          <div>
            <h1 class="text-h3 font-weight-black text-white mb-2">لوحة تحكم الخدمات</h1>
            <p class="text-body-1 text-white-70">إدارة شاملة للخدمات والطلبات الإلكترونية</p>
          </div>
        </div>
        <div class="hero-stats">
          <div class="stat-item" v-for="stat in heroStats" :key="stat.label">
            <span class="stat-value">{{ stat.value }}</span>
            <span class="stat-label">{{ stat.label }}</span>
          </div>
        </div>
      </div>
      <div class="hero-decoration"></div>
    </header>

    <!-- Quick Stats Section -->
    <section class="stats-grid mb-12">
      <v-row>
        <v-col v-for="(card, index) in statsCards" :key="index" cols="12" sm="6" md="3">
          <div class="stat-card" :style="{ '--accent-color': card.color }">
            <div class="stat-card-icon" :style="{ background: card.bgColor }">
              <v-icon :color="card.iconColor" size="32">{{ card.icon }}</v-icon>
            </div>
            <div class="stat-card-content">
              <h3 class="stat-card-value">{{ card.value }}</h3>
              <p class="stat-card-label">{{ card.label }}</p>
              <div class="stat-card-trend" :class="card.trendUp ? 'up' : 'down'">
                <v-icon size="14">{{ card.trendUp ? 'mdi-trending-up' : 'mdi-trending-down' }}</v-icon>
                <span>{{ card.trend }}</span>
              </div>
            </div>
          </div>
        </v-col>
      </v-row>
    </section>

    <!-- Main Content Grid -->
    <v-row>
      <!-- Services Catalog -->
      <v-col cols="12" lg="8">
        <section class="content-section">
          <div class="section-header">
            <div class="d-flex align-center ga-3">
              <div class="section-icon">
                <v-icon color="primary">mdi-apps</v-icon>
              </div>
              <div>
                <h2 class="section-title">كتالوج الخدمات</h2>
                <p class="section-subtitle">جميع الخدمات المتاحة</p>
              </div>
            </div>
            <v-btn variant="text" color="primary" append-icon="mdi-arrow-left" @click="navigateTo('services-catalog')">
              عرض الكل
            </v-btn>
          </div>

          <div class="services-grid">
            <div v-for="service in services" :key="service.id" class="service-card">
              <div class="service-card-header">
                <v-avatar size="48" :color="service.color" variant="tonal">
                  <v-icon>{{ service.icon }}</v-icon>
                </v-avatar>
                <v-chip size="small" :color="service.is_active ? 'success' : 'error'" variant="flat">
                  {{ service.is_active ? 'نشط' : 'غير نشط' }}
                </v-chip>
              </div>
              <h3 class="service-card-title">{{ service.name }}</h3>
              <p class="service-card-category">{{ service.category_name }}</p>
              <p class="service-card-description">{{ service.description }}</p>
              <div class="service-card-footer">
                <v-chip size="x-small" variant="outlined">v{{ service.version }}</v-chip>
                <v-btn size="small" variant="tonal" color="primary" @click="navigateTo('request-service', { fk_service: service.id })">
                  طلب الخدمة
                </v-btn>
              </div>
            </div>
          </div>
        </section>
      </v-col>

      <!-- Quick Actions & Recent Activity -->
      <v-col cols="12" lg="4">
        <!-- Quick Actions -->
        <section class="content-section mb-6">
          <div class="section-header compact">
            <h2 class="section-title">إجراءات سريعة</h2>
          </div>
          <div class="quick-actions-grid">
            <div v-for="action in quickActions" :key="action.label" class="quick-action-card" @click="navigateTo(action.route)">
              <v-avatar :color="action.color" variant="tonal" size="48">
                <v-icon>{{ action.icon }}</v-icon>
              </v-avatar>
              <span class="quick-action-label">{{ action.label }}</span>
            </div>
          </div>
        </section>

        <!-- Recent Requests -->
        <section class="content-section">
          <div class="section-header compact">
            <h2 class="section-title">أحدث الطلبات</h2>
            <v-btn variant="text" size="small" color="primary" @click="navigateTo('my-requests')">
              عرض الكل
            </v-btn>
          </div>
          <div class="recent-requests-list">
            <div v-for="request in recentRequests" :key="request.id" class="request-item">
              <div class="request-item-icon">
                <v-icon :color="getStatusColor(request.status)" size="20">{{ getStatusIcon(request.status) }}</v-icon>
              </div>
              <div class="request-item-content">
                <h4 class="request-item-title">{{ request.service_name }}</h4>
                <p class="request-item-meta">طلب #{{ request.id }} • {{ request.created_at }}</p>
              </div>
              <v-chip size="x-small" :color="getStatusColor(request.status)" variant="flat">
                {{ request.status_display }}
              </v-chip>
            </div>
            <div v-if="recentRequests.length === 0" class="empty-state">
              <v-icon size="48" color="grey-lighten-1">mdi-inbox-outline</v-icon>
              <p>لا توجد طلبات حديثة</p>
            </div>
          </div>
        </section>
      </v-col>
    </v-row>

    <!-- Charts Section -->
    <v-row class="mt-10">
      <!-- Monthly Requests Bar Chart -->
      <v-col cols="12" lg="8">
        <section class="content-section">
          <div class="section-header">
            <div class="d-flex align-center ga-3">
              <div class="section-icon" style="background: #eef2ff;">
                <v-icon color="indigo">mdi-chart-bar</v-icon>
              </div>
              <div>
                <h2 class="section-title">الطلبات الشهرية</h2>
                <p class="section-subtitle">إحصائيات الطلبات خلال الأشهر الماضية</p>
              </div>
            </div>
            <div class="chart-legend">
              <span class="legend-item"><span class="legend-dot" style="background: #2563eb;"></span> مكتملة</span>
              <span class="legend-item"><span class="legend-dot" style="background: #10b981;"></span> معتمدة</span>
              <span class="legend-item"><span class="legend-dot" style="background: #f59e0b;"></span> قيد المعالجة</span>
            </div>
          </div>

          <div class="bar-chart-container">
            <div class="bar-chart">
              <div v-for="(month, index) in monthlyData" :key="index" class="bar-group">
                <div class="bars">
                  <div class="bar completed" :style="{ height: month.completed + '%' }" :title="month.completed + ' مكتملة'"></div>
                  <div class="bar approved" :style="{ height: month.approved + '%' }" :title="month.approved + ' معتمدة'"></div>
                  <div class="bar pending" :style="{ height: month.pending + '%' }" :title="month.pending + ' قيد المعالجة'"></div>
                </div>
                <span class="bar-label">{{ month.name }}</span>
              </div>
            </div>
            <div class="chart-y-axis">
              <span>100</span>
              <span>75</span>
              <span>50</span>
              <span>25</span>
              <span>0</span>
            </div>
          </div>
        </section>
      </v-col>

      <!-- Status Distribution Donut Chart -->
      <v-col cols="12" lg="4">
        <section class="content-section">
          <div class="section-header compact">
            <h2 class="section-title">توزيع حالات الطلبات</h2>
          </div>

          <div class="donut-chart-container">
            <div class="donut-chart">
              <svg viewBox="0 0 36 36" class="circular-chart">
                <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                <path class="circle completed-circle" stroke-dasharray="45, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                <path class="circle approved-circle" stroke-dasharray="25, 100" stroke-dashoffset="-45" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                <path class="circle pending-circle" stroke-dasharray="18, 100" stroke-dashoffset="-70" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                <path class="circle rejected-circle" stroke-dasharray="12, 100" stroke-dashoffset="-88" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
              </svg>
              <div class="donut-center">
                <span class="donut-value">1,045</span>
                <span class="donut-label">طلب</span>
              </div>
            </div>

            <div class="donut-legend">
              <div class="legend-row">
                <span class="legend-color" style="background: #2563eb;"></span>
                <span class="legend-text">مكتملة</span>
                <span class="legend-value">45%</span>
              </div>
              <div class="legend-row">
                <span class="legend-color" style="background: #10b981;"></span>
                <span class="legend-text">معتمدة</span>
                <span class="legend-value">25%</span>
              </div>
              <div class="legend-row">
                <span class="legend-color" style="background: #f59e0b;"></span>
                <span class="legend-text">قيد المعالجة</span>
                <span class="legend-value">18%</span>
              </div>
              <div class="legend-row">
                <span class="legend-color" style="background: #ef4444;"></span>
                <span class="legend-text">مرفوضة</span>
                <span class="legend-value">12%</span>
              </div>
            </div>
          </div>
        </section>
      </v-col>
    </v-row>

    <!-- Activity Timeline & Performance -->
    <v-row class="mt-6">
      <!-- Weekly Activity -->
      <v-col cols="12" md="6">
        <section class="content-section">
          <div class="section-header compact">
            <h2 class="section-title">النشاط الأسبوعي</h2>
          </div>

          <div class="activity-heatmap">
            <div v-for="(day, index) in weeklyActivity" :key="index" class="activity-day">
              <span class="day-name">{{ day.name }}</span>
              <div class="activity-bars">
                <div
                  v-for="(hour, hIndex) in day.hours"
                  :key="hIndex"
                  class="activity-cell"
                  :class="getActivityLevel(hour)"
                  :title="hour + ' طلب'"
                ></div>
              </div>
              <span class="day-total">{{ day.total }}</span>
            </div>
          </div>

          <div class="activity-legend">
            <span class="text-caption text-grey">أقل</span>
            <div class="activity-scale">
              <span class="scale-cell level-0"></span>
              <span class="scale-cell level-1"></span>
              <span class="scale-cell level-2"></span>
              <span class="scale-cell level-3"></span>
              <span class="scale-cell level-4"></span>
            </div>
            <span class="text-caption text-grey">أكثر</span>
          </div>
        </section>
      </v-col>

      <!-- Performance Metrics -->
      <v-col cols="12" md="6">
        <section class="content-section">
          <div class="section-header compact">
            <h2 class="section-title">مؤشرات الأداء</h2>
          </div>

          <div class="performance-metrics">
            <div v-for="metric in performanceMetrics" :key="metric.label" class="metric-item">
              <div class="metric-header">
                <span class="metric-label">{{ metric.label }}</span>
                <span class="metric-value" :style="{ color: metric.color }">{{ metric.value }}</span>
              </div>
              <div class="metric-bar-bg">
                <div class="metric-bar-fill" :style="{ width: metric.percentage + '%', background: metric.color }"></div>
              </div>
              <span class="metric-target">الهدف: {{ metric.target }}</span>
            </div>
          </div>
        </section>
      </v-col>
    </v-row>

    <!-- Categories Overview -->
    <section class="content-section mt-10">
      <div class="section-header">
        <div class="d-flex align-center ga-3">
          <div class="section-icon">
            <v-icon color="primary">mdi-shape-outline</v-icon>
          </div>
          <div>
            <h2 class="section-title">تصنيفات الخدمات</h2>
            <p class="section-subtitle">استعراض الخدمات حسب التصنيف</p>
          </div>
        </div>
      </div>
      <v-row>
        <v-col v-for="category in categories" :key="category.id" cols="12" sm="6" md="4" lg="3">
          <div class="category-card" @click="filterByCategory(category.id)">
            <div class="category-card-icon" :style="{ background: category.bgColor }">
              <v-icon :color="category.iconColor" size="28">{{ category.icon }}</v-icon>
            </div>
            <div class="category-card-content">
              <h3 class="category-card-title">{{ category.name }}</h3>
              <p class="category-card-count">{{ category.services_count }} خدمة</p>
            </div>
            <v-icon color="grey-lighten-1" size="20">mdi-chevron-left</v-icon>
          </div>
        </v-col>
      </v-row>
    </section>
  </div>
</template>

<script>
export default {
  name: 'ServicesDashboard',
  data() {
    return {
      loading: false,
      services: [
        {
          id: 1,
          name: 'طلب شهادة تخرج',
          category_name: 'الشهادات والوثائق',
          description: 'خدمة استخراج شهادة التخرج الرسمية للطلاب الخريجين من الجامعة',
          version: '2.1',
          is_active: true,
          icon: 'mdi-school',
          color: 'primary'
        },
        {
          id: 2,
          name: 'طلب كشف درجات',
          category_name: 'الشهادات والوثائق',
          description: 'استخراج كشف الدرجات الأكاديمي الرسمي للفصول الدراسية',
          version: '1.5',
          is_active: true,
          icon: 'mdi-file-document',
          color: 'success'
        },
        {
          id: 3,
          name: 'طلب تحويل داخلي',
          category_name: 'التحويلات الأكاديمية',
          description: 'التحويل بين الأقسام والكليات داخل الجامعة',
          version: '3.0',
          is_active: true,
          icon: 'mdi-swap-horizontal',
          color: 'amber-darken-2'
        },
        {
          id: 4,
          name: 'طلب إعادة قيد',
          category_name: 'شؤون الطلاب',
          description: 'إعادة القيد للطلاب المنقطعين عن الدراسة',
          version: '1.2',
          is_active: true,
          icon: 'mdi-account-arrow-right',
          color: 'indigo'
        },
        {
          id: 5,
          name: 'طلب تأجيل دراسة',
          category_name: 'شؤون الطلاب',
          description: 'تأجيل الفصل الدراسي لظروف خاصة',
          version: '2.0',
          is_active: true,
          icon: 'mdi-calendar-clock',
          color: 'teal'
        },
        {
          id: 6,
          name: 'طلب منحة دراسية',
          category_name: 'الشؤون المالية',
          description: 'التقديم على المنح الدراسية والإعفاءات المالية',
          version: '1.8',
          is_active: true,
          icon: 'mdi-cash-multiple',
          color: 'pink'
        }
      ],
      categories: [
        { id: 1, name: 'الشهادات والوثائق', services_count: 8, icon: 'mdi-certificate', bgColor: '#eff6ff', iconColor: 'primary' },
        { id: 2, name: 'شؤون الطلاب', services_count: 12, icon: 'mdi-account-group', bgColor: '#ecfdf5', iconColor: 'success' },
        { id: 3, name: 'الشؤون المالية', services_count: 5, icon: 'mdi-cash-multiple', bgColor: '#fffbeb', iconColor: 'amber-darken-2' },
        { id: 4, name: 'التحويلات الأكاديمية', services_count: 4, icon: 'mdi-swap-horizontal', bgColor: '#eef2ff', iconColor: 'indigo' },
        { id: 5, name: 'التسجيل والقبول', services_count: 6, icon: 'mdi-file-cog', bgColor: '#fdf2f8', iconColor: 'pink' },
        { id: 6, name: 'المكتبة والبحث العلمي', services_count: 3, icon: 'mdi-book-education', bgColor: '#f0fdf4', iconColor: 'teal' }
      ],
      recentRequests: [
        { id: 1045, service_name: 'طلب شهادة تخرج', status: 'pending', status_display: 'قيد المراجعة', created_at: '2026-01-07' },
        { id: 1044, service_name: 'طلب كشف درجات', status: 'approved', status_display: 'معتمد', created_at: '2026-01-06' },
        { id: 1043, service_name: 'طلب تحويل داخلي', status: 'processing', status_display: 'قيد المعالجة', created_at: '2026-01-05' },
        { id: 1042, service_name: 'طلب منحة دراسية', status: 'completed', status_display: 'مكتمل', created_at: '2026-01-04' },
        { id: 1041, service_name: 'طلب إعادة قيد', status: 'rejected', status_display: 'مرفوض', created_at: '2026-01-03' }
      ],
      stats: {
        totalServices: 38,
        totalRequests: 1045,
        pendingRequests: 127,
        completedRequests: 856
      },
      monthlyData: [
        { name: 'يناير', completed: 75, approved: 45, pending: 30 },
        { name: 'فبراير', completed: 82, approved: 52, pending: 25 },
        { name: 'مارس', completed: 68, approved: 48, pending: 35 },
        { name: 'أبريل', completed: 90, approved: 60, pending: 20 },
        { name: 'مايو', completed: 85, approved: 55, pending: 28 },
        { name: 'يونيو', completed: 95, approved: 65, pending: 22 }
      ],
      weeklyActivity: [
        { name: 'السبت', hours: [5, 12, 18, 25, 15, 8, 3], total: 86 },
        { name: 'الأحد', hours: [8, 22, 35, 28, 20, 12, 5], total: 130 },
        { name: 'الاثنين', hours: [10, 25, 40, 32, 22, 15, 8], total: 152 },
        { name: 'الثلاثاء', hours: [12, 28, 38, 30, 25, 18, 10], total: 161 },
        { name: 'الأربعاء', hours: [15, 30, 42, 35, 28, 20, 12], total: 182 },
        { name: 'الخميس', hours: [8, 18, 28, 22, 15, 10, 5], total: 106 },
        { name: 'الجمعة', hours: [2, 5, 8, 6, 4, 2, 1], total: 28 }
      ],
      performanceMetrics: [
        { label: 'معدل إنجاز الطلبات', value: '92%', percentage: 92, target: '90%', color: '#10b981' },
        { label: 'متوسط وقت المعالجة', value: '2.3 يوم', percentage: 78, target: '2 يوم', color: '#f59e0b' },
        { label: 'رضا العملاء', value: '4.7/5', percentage: 94, target: '4.5/5', color: '#2563eb' },
        { label: 'الطلبات المعلقة', value: '127', percentage: 35, target: '< 100', color: '#ef4444' }
      ]
    };
  },
  computed: {
    heroStats() {
      return [
        { value: this.stats.totalServices, label: 'خدمة متاحة' },
        { value: this.stats.totalRequests, label: 'طلب إجمالي' },
        { value: this.stats.pendingRequests, label: 'قيد المعالجة' }
      ];
    },
    statsCards() {
      return [
        {
          label: 'الخدمات النشطة',
          value: this.stats.totalServices,
          icon: 'mdi-cog-outline',
          color: '#2563eb',
          bgColor: '#eff6ff',
          iconColor: 'primary',
          trend: '+12%',
          trendUp: true
        },
        {
          label: 'الطلبات الجديدة',
          value: this.stats.pendingRequests,
          icon: 'mdi-file-document-plus-outline',
          color: '#f59e0b',
          bgColor: '#fffbeb',
          iconColor: 'amber-darken-2',
          trend: '+5%',
          trendUp: true
        },
        {
          label: 'الطلبات المكتملة',
          value: this.stats.completedRequests,
          icon: 'mdi-check-decagram-outline',
          color: '#10b981',
          bgColor: '#ecfdf5',
          iconColor: 'success',
          trend: '+8%',
          trendUp: true
        },
        {
          label: 'إجمالي الطلبات',
          value: this.stats.totalRequests,
          icon: 'mdi-chart-box-outline',
          color: '#6366f1',
          bgColor: '#eef2ff',
          iconColor: 'indigo',
          trend: '+15%',
          trendUp: true
        }
      ];
    },
    quickActions() {
      return [
        { icon: 'mdi-plus-circle-outline', label: 'طلب جديد', color: 'primary', route: 'services-catalog' },
        { icon: 'mdi-history', label: 'طلباتي', color: 'amber-darken-2', route: 'my-requests' },
        { icon: 'mdi-cog-outline', label: 'الإعدادات', color: 'grey', route: 'settings' },
        { icon: 'mdi-help-circle-outline', label: 'المساعدة', color: 'info', route: 'help' }
      ];
    }
  },
  async created() {
    // Data is already initialized with mock values
    // Optionally try to load real data from API
    // await this.loadDashboardData();
  },
  methods: {
    async loadDashboardData() {
      // Keep mock data - API calls can override if available
    },
    navigateTo(routeName, query = null) {
      this.$router.push({ name: routeName, query });
    },
    filterByCategory(categoryId) {
      this.$router.push({ name: 'services-catalog', query: { category: categoryId } });
    },
    getStatusColor(status) {
      const colors = {
        pending: 'warning',
        processing: 'info',
        approved: 'success',
        rejected: 'error',
        completed: 'success'
      };
      return colors[status] || 'grey';
    },
    getStatusIcon(status) {
      const icons = {
        pending: 'mdi-clock-outline',
        processing: 'mdi-progress-clock',
        approved: 'mdi-check-circle',
        rejected: 'mdi-close-circle',
        completed: 'mdi-check-decagram'
      };
      return icons[status] || 'mdi-circle';
    },
    getServiceIcon(index) {
      const icons = ['mdi-school', 'mdi-file-document', 'mdi-certificate', 'mdi-book-open', 'mdi-account-card', 'mdi-cash'];
      return icons[index % icons.length];
    },
    getServiceColor(index) {
      const colors = ['primary', 'success', 'amber-darken-2', 'indigo', 'teal', 'pink'];
      return colors[index % colors.length];
    },
    getCategoryIcon(index) {
      const icons = ['mdi-school', 'mdi-account-group', 'mdi-cash-multiple', 'mdi-certificate', 'mdi-file-cog', 'mdi-book-education'];
      return icons[index % icons.length];
    },
    getCategoryBgColor(index) {
      const colors = ['#eff6ff', '#ecfdf5', '#fffbeb', '#eef2ff', '#fdf2f8', '#f0fdf4'];
      return colors[index % colors.length];
    },
    getCategoryIconColor(index) {
      const colors = ['primary', 'success', 'amber-darken-2', 'indigo', 'pink', 'teal'];
      return colors[index % colors.length];
    },
    getActivityLevel(value) {
      if (value === 0) return 'level-0';
      if (value <= 10) return 'level-1';
      if (value <= 25) return 'level-2';
      if (value <= 35) return 'level-3';
      return 'level-4';
    }
  }
};
</script>

<style scoped>
.services-dashboard {
  max-width: 1600px;
  margin: 0 auto;
  padding: 24px;
}

/* Hero Header */
.dashboard-hero {
  background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
  border-radius: 24px;
  padding: 48px;
  position: relative;
  overflow: hidden;
}

.hero-content {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 32px;
}

.hero-icon-wrapper {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  /* backdrop-filter: blur(10px); */
}

.text-white-70 {
  color: rgba(255, 255, 255, 0.7);
}

.hero-stats {
  display: flex;
  gap: 48px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 2.5rem;
  font-weight: 900;
  color: white;
  line-height: 1;
}

.stat-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
  font-weight: 500;
  margin-top: 8px;
}

.hero-decoration {
  position: absolute;
  top: -50%;
  right: -10%;
  width: 400px;
  height: 400px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 50%;
}

/* Stats Cards */
.stats-grid {
  margin-top: -32px;
  position: relative;
  z-index: 3;
}

.stat-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
  border: 1px solid #f1f5f9;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
}

.stat-card-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-card-value {
  font-size: 1.75rem;
  font-weight: 900;
  color: #0f172a;
  margin: 0;
  line-height: 1;
}

.stat-card-label {
  font-size: 0.875rem;
  color: #64748b;
  margin: 4px 0;
}

.stat-card-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

.stat-card-trend.up {
  color: #10b981;
}

.stat-card-trend.down {
  color: #ef4444;
}

/* Content Sections */
.content-section {
  background: white;
  border-radius: 24px;
  padding: 32px;
  border: 1px solid #f1f5f9;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-header.compact {
  margin-bottom: 16px;
}

.section-icon {
  width: 48px;
  height: 48px;
  background: #eff6ff;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 900;
  color: #0f172a;
  margin: 0;
}

.section-subtitle {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
}

/* Services Grid */
.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.service-card {
  background: #f8fafc;
  border-radius: 20px;
  padding: 24px;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.service-card:hover {
  background: white;
  border-color: #e2e8f0;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
}

.service-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.service-card-title {
  font-size: 1rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 4px;
}

.service-card-category {
  font-size: 0.75rem;
  color: #64748b;
  margin: 0 0 12px;
}

.service-card-description {
  font-size: 0.875rem;
  color: #475569;
  line-height: 1.6;
  margin: 0 0 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.service-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Quick Actions */
.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.quick-action-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.quick-action-card:hover {
  background: #eff6ff;
  transform: translateY(-2px);
}

.quick-action-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #334155;
}

/* Recent Requests */
.recent-requests-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.request-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 12px;
  transition: background 0.2s;
}

.request-item:hover {
  background: #f1f5f9;
}

.request-item-icon {
  width: 36px;
  height: 36px;
  background: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.request-item-content {
  flex: 1;
  min-width: 0;
}

.request-item-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.request-item-meta {
  font-size: 0.75rem;
  color: #64748b;
  margin: 0;
}

/* Categories */
.category-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.category-card:hover {
  background: white;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.category-card-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.category-card-content {
  flex: 1;
}

.category-card-title {
  font-size: 1rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.category-card-count {
  font-size: 0.875rem;
  color: #64748b;
  margin: 4px 0 0;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 32px;
  color: #94a3b8;
}

.empty-state p {
  margin-top: 12px;
  font-size: 0.875rem;
}

/* Responsive */
@media (max-width: 960px) {
  .dashboard-hero {
    padding: 32px;
  }

  .hero-stats {
    gap: 24px;
  }

  .stat-value {
    font-size: 1.75rem;
  }
}

@media (max-width: 600px) {
  .services-dashboard {
    padding: 16px;
  }

  .dashboard-hero {
    padding: 24px;
  }

  .hero-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .hero-stats {
    width: 100%;
    justify-content: space-between;
  }

  .content-section {
    padding: 20px;
  }
}

/* Charts Styles */
.chart-legend {
  display: flex;
  gap: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  color: #64748b;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

/* Bar Chart */
.bar-chart-container {
  display: flex;
  gap: 16px;
  height: 250px;
  padding-top: 20px;
}

.bar-chart {
  flex: 1;
  display: flex;
  justify-content: space-around;
  align-items: flex-end;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 8px;
}

.bar-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.bars {
  display: flex;
  gap: 4px;
  align-items: flex-end;
  height: 200px;
}

.bar {
  width: 16px;
  border-radius: 4px 4px 0 0;
  transition: height 0.5s ease;
  cursor: pointer;
}

.bar:hover {
  opacity: 0.8;
}

.bar.completed { background: #2563eb; }
.bar.approved { background: #10b981; }
.bar.pending { background: #f59e0b; }

.bar-label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
}

.chart-y-axis {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-size: 0.7rem;
  color: #94a3b8;
  padding-bottom: 24px;
}

/* Donut Chart */
.donut-chart-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.donut-chart {
  position: relative;
  width: 180px;
  height: 180px;
}

.circular-chart {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.circle-bg {
  fill: none;
  stroke: #f1f5f9;
  stroke-width: 3;
}

.circle {
  fill: none;
  stroke-width: 3;
  stroke-linecap: round;
  animation: progress 1s ease-out forwards;
}

.completed-circle { stroke: #2563eb; }
.approved-circle { stroke: #10b981; }
.pending-circle { stroke: #f59e0b; }
.rejected-circle { stroke: #ef4444; }

@keyframes progress {
  0% { stroke-dasharray: 0, 100; }
}

.donut-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.donut-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 900;
  color: #0f172a;
}

.donut-label {
  font-size: 0.875rem;
  color: #64748b;
}

.donut-legend {
  width: 100%;
}

.legend-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #f1f5f9;
}

.legend-row:last-child {
  border-bottom: none;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 4px;
}

.legend-text {
  flex: 1;
  font-size: 0.875rem;
  color: #334155;
}

.legend-value {
  font-size: 0.875rem;
  font-weight: 700;
  color: #0f172a;
}

/* Activity Heatmap */
.activity-heatmap {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.activity-day {
  display: flex;
  align-items: center;
  gap: 12px;
}

.day-name {
  width: 60px;
  font-size: 0.75rem;
  color: #64748b;
  text-align: right;
}

.activity-bars {
  display: flex;
  gap: 4px;
  flex: 1;
}

.activity-cell {
  flex: 1;
  height: 24px;
  border-radius: 4px;
  cursor: pointer;
  transition: transform 0.2s;
}

.activity-cell:hover {
  transform: scale(1.1);
}

.activity-cell.level-0 { background: #f1f5f9; }
.activity-cell.level-1 { background: #bfdbfe; }
.activity-cell.level-2 { background: #60a5fa; }
.activity-cell.level-3 { background: #2563eb; }
.activity-cell.level-4 { background: #1d4ed8; }

.day-total {
  width: 40px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #334155;
  text-align: left;
}

.activity-legend {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 16px;
}

.activity-scale {
  display: flex;
  gap: 4px;
}

.scale-cell {
  width: 16px;
  height: 16px;
  border-radius: 3px;
}

/* Performance Metrics */
.performance-metrics {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.metric-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.metric-label {
  font-size: 0.875rem;
  color: #334155;
  font-weight: 500;
}

.metric-value {
  font-size: 1rem;
  font-weight: 800;
}

.metric-bar-bg {
  height: 8px;
  background: #f1f5f9;
  border-radius: 4px;
  overflow: hidden;
}

.metric-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.8s ease;
}

.metric-target {
  font-size: 0.7rem;
  color: #94a3b8;
}
</style>
