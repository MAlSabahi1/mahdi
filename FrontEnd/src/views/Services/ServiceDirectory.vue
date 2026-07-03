<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="دليل الخدمات والاستمارات المعتمدة (24 كرت خدمة)" />

    <div class="space-y-8 text-start animate-fade-in" dir="rtl">
      
      <!-- Modern Hero Panel with Mesh Gradient Background -->
      <div class="relative overflow-hidden rounded-3xl border border-gray-200 dark:border-gray-800 bg-gradient-to-br from-gray-900 via-gray-950 to-brand-950 p-8 text-white shadow-xl">
        <div class="absolute -right-20 -top-20 w-72 h-72 bg-brand-500/10 rounded-full blur-3xl pointer-events-none animate-pulse"></div>
        <div class="absolute left-10 bottom-0 w-60 h-60 bg-emerald-500/5 rounded-full blur-3xl pointer-events-none"></div>
        
        <div class="relative flex flex-col md:flex-row justify-between items-start md:items-center gap-6 z-10">
          <div class="flex items-center gap-5">
            <div class="p-4 bg-white/10 backdrop-blur-md text-brand-400 rounded-2xl border border-white/10 shadow-lg">
              <LayoutGrid class="h-8 w-8 stroke-[1.5]" />
            </div>
            <div>
              <span class="text-[10px] font-bold tracking-widest text-brand-400 uppercase bg-brand-500/10 px-3 py-1 rounded-full border border-brand-500/20">
                بوابة الخدمات الرسمية
              </span>
              <h1 class="text-2xl font-black text-white mt-2">
                دليل كروت الخدمات والاستمارات المعتمدة
              </h1>
              <p class="text-xs text-gray-400 mt-1 max-w-xl leading-relaxed">
                دليل تفصيلي يوثق كافة كروت الخدمة الـ 24 المعتمدة رسمياً في النظام لتقديم الطلبات الإدارية وحركات القوة وتنظيم الشؤون المالية والانضباطية.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Grid (Sovereign Widgets) -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <div 
          v-for="stat in stats" 
          :key="stat.label"
          class="relative overflow-hidden bg-white dark:bg-gray-900 p-5 border border-gray-200 dark:border-gray-800 rounded-2xl shadow-sm hover:shadow-md transition-all duration-300 group"
        >
          <!-- Subtle hover orb -->
          <div class="absolute -right-8 -bottom-8 w-20 h-20 bg-gray-500/5 rounded-full blur-xl group-hover:scale-125 transition-transform duration-500 pointer-events-none"></div>
          
          <div class="relative flex items-center justify-between">
            <div>
              <p class="text-[11px] font-bold text-gray-400 dark:text-gray-500 mb-1.5 uppercase tracking-wider">{{ stat.label }}</p>
              <p class="text-2xl font-black text-gray-900 dark:text-white font-mono leading-none">{{ stat.value }}</p>
            </div>
            <div :class="[stat.colorClass]" class="p-3.5 rounded-2xl border transition-all duration-300 group-hover:scale-110">
              <component :is="stat.icon" class="w-6 h-6" />
            </div>
          </div>
        </div>
      </div>

      <!-- Glassmorphic Control Panel (Filters & Search) -->
      <div class="bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border border-gray-200 dark:border-gray-800 rounded-2xl p-4 shadow-sm flex flex-col md:flex-row gap-4 items-center justify-between relative z-20">
        <!-- Categories Tabs -->
        <div class="flex flex-wrap gap-2 w-full md:w-auto">
          <button 
            v-for="cat in categories" 
            :key="cat.id" 
            @click="selectedCategory = cat.id"
            :class="[
              selectedCategory === cat.id 
                ? 'bg-brand-600 text-white shadow-md shadow-brand-500/20 border-brand-500/10' 
                : 'bg-gray-50 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-750 border-gray-200/40 dark:border-gray-700/40'
            ]"
            class="px-4 py-2.5 text-xs font-black rounded-xl transition-all cursor-pointer border"
          >
            {{ cat.label }}
          </button>
        </div>
        
        <!-- Search Input with Glow effect on focus -->
        <div class="relative w-full md:w-80 group">
          <span class="absolute inset-y-0 right-0 flex items-center pr-3.5 pointer-events-none text-gray-400 group-focus-within:text-brand-500 transition-colors">
            <Search class="h-4 w-4" />
          </span>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="البحث بالاسم أو الرقم أو وصف الكرت..." 
            class="w-full text-xs pr-10 pl-4 py-2.5 border border-gray-200 dark:border-gray-800 rounded-xl bg-gray-50/50 dark:bg-gray-850 text-gray-700 dark:text-gray-300 focus:border-brand-500 focus:ring-4 focus:ring-brand-500/10 focus:bg-white dark:focus:bg-gray-900 transition-all outline-none"
          />
          <button 
            v-if="searchQuery"
            @click="searchQuery = ''"
            class="absolute inset-y-0 left-0 flex items-center pl-3.5 text-gray-400 hover:text-gray-600"
          >
            ×
          </button>
        </div>
      </div>

      <!-- Cards Grid with Floating Side Bars and Hover Orbs -->
      <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <div 
          v-for="card in filteredCards" 
          :key="card.id" 
          class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-sm hover:shadow-xl hover:shadow-brand-500/5 hover:-translate-y-1.5 transition-all duration-500 ease-out group relative overflow-hidden flex flex-col h-full"
        >
          <!-- Floating sidebar color indicator -->
          <div 
            class="absolute right-0 top-1/2 -translate-y-1/2 w-1.5 h-12 rounded-l-full transition-all duration-500 group-hover:h-20"
            :class="[
              card.type === 'military' ? 'bg-blue-600 dark:bg-blue-500' : 
              card.type === 'financial' ? 'bg-emerald-600 dark:bg-emerald-500' :
              'bg-rose-600 dark:bg-rose-500'
            ]"
          ></div>

          <!-- Bottom-Right Glowing Orb -->
          <div 
            class="absolute -right-10 -bottom-10 w-24 h-24 rounded-full blur-2xl opacity-0 group-hover:opacity-20 dark:group-hover:opacity-30 transition-opacity duration-500 pointer-events-none"
            :class="[
              card.type === 'military' ? 'bg-blue-500' :
              card.type === 'financial' ? 'bg-emerald-500' :
              'bg-rose-500'
            ]"
          ></div>

          <!-- Card Header Section -->
          <div class="flex justify-between items-start mb-5 relative z-10">
            <!-- Icon box with custom radial gradient and hover pulse -->
            <div 
              class="w-13 h-13 rounded-2xl flex items-center justify-center border transition-all duration-300 group-hover:scale-105"
              :class="[
                card.type === 'military' ? 'bg-gradient-to-br from-blue-50 to-blue-100/50 border-blue-200/60 text-blue-600 dark:from-blue-950/20 dark:to-blue-900/5 dark:border-blue-900/40 dark:text-blue-400' :
                card.type === 'financial' ? 'bg-gradient-to-br from-emerald-50 to-emerald-100/50 border-emerald-200/60 text-emerald-600 dark:from-emerald-950/20 dark:to-emerald-900/5 dark:border-emerald-900/40 dark:text-emerald-400' :
                'bg-gradient-to-br from-rose-50 to-rose-100/50 border-rose-200/60 text-rose-600 dark:from-rose-950/20 dark:to-rose-900/5 dark:border-rose-900/40 dark:text-rose-400'
              ]"
            >
              <component :is="card.icon" class="w-6 h-6 stroke-[1.5]" />
            </div>
            
            <div class="flex flex-col items-end gap-1.5">
              <span class="text-[9px] font-mono font-bold text-gray-400 bg-gray-50 border border-gray-150 px-2.5 py-0.5 rounded dark:bg-gray-800 dark:border-gray-700 dark:text-gray-450">
                كرت #{{ card.cardNumber }}
              </span>
              <span 
                class="text-[9px] font-bold px-2 py-0.5 rounded-full"
                :class="[
                  card.type === 'military' ? 'bg-blue-50 text-blue-700 dark:bg-blue-950/40 dark:text-blue-300' :
                  card.type === 'financial' ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300' :
                  'bg-rose-50 text-rose-700 dark:bg-rose-950/40 dark:text-rose-300'
                ]"
              >
                {{ card.type === 'military' ? 'حركة وتعيين' : card.type === 'financial' ? 'مالي واستحقاق' : 'شؤون انضباطية' }}
              </span>
            </div>
          </div>

          <!-- Card Body -->
          <div class="flex-1 relative z-10 flex flex-col justify-between">
            <div class="space-y-2">
              <h3 class="font-black text-sm text-gray-950 dark:text-white group-hover:text-brand-650 dark:group-hover:text-brand-400 transition-colors duration-300">
                {{ card.title }}
              </h3>
              <p class="text-xs text-gray-500 dark:text-gray-400 leading-relaxed line-clamp-2">
                {{ card.desc }}
              </p>
            </div>

            <!-- Horizontal Meta Pills -->
            <div class="flex flex-wrap gap-2 mt-5 pt-4 border-t border-gray-100 dark:border-gray-850">
              <div class="flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-gray-50/50 dark:bg-gray-800/40 border border-gray-100 dark:border-gray-800 text-[10px] text-gray-500 dark:text-gray-400">
                <Paperclip class="w-3 h-3 text-gray-400" />
                <span>المرفقات: {{ card.attachmentsCount }}</span>
              </div>
              <div class="flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-gray-50/50 dark:bg-gray-800/40 border border-gray-100 dark:border-gray-800 text-[10px] text-gray-500 dark:text-gray-400">
                <Clock class="w-3 h-3 text-gray-400" />
                <span>المدة: {{ card.duration }}</span>
              </div>
              <div class="flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-gray-50/50 dark:bg-gray-800/40 border border-gray-100 dark:border-gray-800 text-[10px] text-gray-500 dark:text-gray-400">
                <UserCheck class="w-3 h-3 text-gray-400" />
                <span>{{ card.target }}</span>
              </div>
            </div>
          </div>

          <!-- Card Footer (CTA Button Overhaul) -->
          <div class="mt-5 pt-4 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between relative z-10">
            <span class="inline-flex items-center gap-1 text-[9px] font-bold text-emerald-600 dark:text-emerald-400">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              معتمد للتقديم
            </span>

            <RouterLink 
              to="/services/request"
              class="relative overflow-hidden inline-flex items-center gap-1.5 px-4 py-2 text-xs font-black rounded-xl border transition-all duration-300 cursor-pointer"
              :class="[
                card.type === 'military' ? 'bg-blue-500/5 border-blue-500/10 text-blue-600 dark:text-blue-450 hover:bg-blue-600 hover:text-white hover:border-transparent hover:shadow-lg hover:shadow-blue-500/20' :
                card.type === 'financial' ? 'bg-emerald-500/5 border-emerald-500/10 text-emerald-600 dark:text-emerald-450 hover:bg-emerald-600 hover:text-white hover:border-transparent hover:shadow-lg hover:shadow-emerald-500/20' :
                'bg-rose-500/5 border-rose-500/10 text-rose-600 dark:text-rose-450 hover:bg-rose-600 hover:text-white hover:border-transparent hover:shadow-lg hover:shadow-rose-500/20'
              ]"
            >
              <span>تقديم طلب</span>
              <ArrowLeft class="w-3.5 h-3.5 transition-transform duration-300 group-hover:-translate-x-1" />
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- Empty Search State -->
      <div v-if="filteredCards.length === 0" class="flex flex-col items-center justify-center py-20 text-center border rounded-2xl bg-white dark:bg-gray-900 border-dashed dark:border-gray-800">
        <div class="w-16 h-16 rounded-full bg-brand-500/10 text-brand-600 flex items-center justify-center mb-4">
          <LayoutGrid class="w-8 h-8 opacity-80" />
        </div>
        <h3 class="text-lg font-black mb-2 text-gray-900 dark:text-white">
          لا توجد كروت خدمات تطابق البحث
        </h3>
        <p class="text-xs text-gray-400 max-w-sm">
          جرب كتابة كلمة أخرى في شريط البحث أو تغيير تبويب الفلتر المعروض.
        </p>
      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { 
  // Base structural icons
  Search, Users, Coins, ShieldAlert, Clock, Paperclip, UserCheck, ArrowLeft, LayoutGrid,
  // Unique service icons mapped to each card
  Award, TrendingUp, LogOut, PauseCircle, MapPin, Percent, Home, AlertOctagon,
  HeartHandshake, Binary, GraduationCap, CalendarCheck, History, ShieldCheck,
  Briefcase, Activity, ExternalLink, Reply, Globe, FileText, FileX, UserPlus
} from 'lucide-vue-next'

const selectedCategory = ref('all')
const searchQuery = ref('')

const categories = [
  { id: 'all', label: 'كل الكروت (24)' },
  { id: 'military', label: 'حركات الأفراد والتعيينات' },
  { id: 'financial', label: 'الخدمات المالية والرواتب' },
  { id: 'disciplinary', label: 'شؤون الانضباط والإجراءات' }
]

interface ServiceCard {
  id: number
  cardNumber: string
  title: string
  desc: string
  type: 'military' | 'financial' | 'disciplinary'
  attachmentsCount: number
  duration: string
  target: string
  icon: any
}

// 24 highly detailed, official service cards with no "عسكري" mentions
const serviceCards = ref<ServiceCard[]>([
  { id: 1, cardNumber: '01', title: 'طلب تسوية رتبة', desc: 'معالجة تسويات الوضع وتعديل الرتبة المستحقة للأفراد والضباط بناءً على قرارات تسوية الأوضاع القيادية.', type: 'military', attachmentsCount: 3, duration: '48 ساعة', target: 'الكل', icon: Award },
  { id: 2, cardNumber: '02', title: 'طلب علاوة رتبة جديدة', desc: 'تفعيل وصرف علاوة الرتبة الجديدة المترتبة على قرارات الترقية أو تسوية الوضع المالي للمنتسب.', type: 'financial', attachmentsCount: 2, duration: '24 ساعة', target: 'الكل', icon: TrendingUp },
  { id: 3, cardNumber: '03', title: 'طلب إحالة للتقاعد المبكر', desc: 'حصر الخدمات وتسوية المبالغ المستحقة للتقاعد النظامي ورفع الملف للإدارة المختصة.', type: 'military', attachmentsCount: 4, duration: '72 ساعة', target: 'ضباط وأفراد', icon: LogOut },
  { id: 4, cardNumber: '04', title: 'طلب تجميد الراتب المؤقت', desc: 'إيقاف المعالجة المالية للفرد لغيابه أو انقطاعه عن العمل لرفع كشوف الرد والتنزيلات.', type: 'financial', attachmentsCount: 1, duration: '12 ساعة', target: 'الكل', icon: PauseCircle },
  { id: 5, cardNumber: '05', title: 'طلب نقل جغرافي وإداري', desc: 'نقل المنتسب إدارياً وجغرافياً وتعديل صلاحيات النطاق والـ ABAC التابع له بالمحافظات.', type: 'military', attachmentsCount: 2, duration: '24 ساعة', target: 'الكل', icon: MapPin },
  { id: 6, cardNumber: '06', title: 'إجراء جزائي مالي (عقوبة)', desc: 'حسم مبالغ محددة من البدلات أو الراتب الأساسي لقاء مخالفات انضباطية موثقة ومعتمدة.', type: 'disciplinary', attachmentsCount: 3, duration: '24 ساعة', target: 'الكل', icon: Percent },
  { id: 7, cardNumber: '07', title: 'طلب بدل سكن وإقامة نائية', desc: 'صرف بدلات إضافية مخصصة للمناطق ذات الظروف الميدانية الصعبة والنائية بالمحافظات.', type: 'financial', attachmentsCount: 2, duration: '48 ساعة', target: 'أفراد فقط', icon: Home },
  { id: 8, cardNumber: '08', title: 'إثبات حالة فرار أو غياب رسمي', desc: 'إصدار أمر إيقاف الخدمة وتحويل ملف الفرد للشؤون القانونية واللجنة المختصة.', type: 'disciplinary', attachmentsCount: 3, duration: '12 ساعة', target: 'الكل', icon: AlertOctagon },
  { id: 9, cardNumber: '09', title: 'طلب صرف إعانة وفاة أثناء الخدمة', desc: 'معاملة عاجلة لصرف الإعانات الاستثنائية لورثة المنتسب المتوفى أثناء أداء الواجب الرسمي.', type: 'financial', attachmentsCount: 5, duration: '24 ساعة', target: 'ضباط وأفراد', icon: HeartHandshake },
  { id: 10, cardNumber: '10', title: 'طلب استثناء فني للرقم المالي', desc: 'معالجة حالات تكرار الأرقام الوظيفية أو الأخطاء الهيكلية الواردة بكشوفات الإدارة.', type: 'financial', attachmentsCount: 1, duration: '24 ساعة', target: 'الكل', icon: Binary },
  { id: 11, cardNumber: '11', title: 'طلب تسوية بعد التأهيل الدراسي', desc: 'تحديث المؤهل الدراسي في الملف الشخصي وإعادة احتساب الراتب والموقع طبقاً للمستجدات.', type: 'military', attachmentsCount: 2, duration: '48 ساعة', target: 'الكل', icon: GraduationCap },
  { id: 12, cardNumber: '12', title: 'إقرار عودة من إجازة طويلة', desc: 'إعادة تفعيل صرف الراتب وإعادة الإدراج في الكشوف الجارية بعد الانقطاع المعتمد.', type: 'military', attachmentsCount: 2, duration: '24 ساعة', target: 'الكل', icon: CalendarCheck },
  { id: 13, cardNumber: '13', title: 'طلب ضم سنوات خدمة سابقة', desc: 'احتساب سنوات الخدمة السابقة في قطاع الخدمة الأمنية وتأثيرها على الأقدمية والراتب.', type: 'military', attachmentsCount: 3, duration: '72 ساعة', target: 'ضباط وأفراد', icon: History },
  { id: 14, cardNumber: '14', title: 'طلب ترقية استثنائية للشهداء والجرحى', desc: 'ترقية الفرد للرتبة التالية مباشرة استثنائياً تقديراً للتضحيات أثناء الواجب الرسمي.', type: 'military', attachmentsCount: 4, duration: '24 ساعة', target: 'ضباط وأفراد', icon: ShieldCheck },
  { id: 15, cardNumber: '15', title: 'طلب صرف بدل طبيعة عمل', desc: 'صرف بدل مالي تخصصي للوظائف الفنية والتقنية التي تتطلب مهارات تخصصية خاصة.', type: 'financial', attachmentsCount: 2, duration: '48 ساعة', target: 'الكل', icon: Briefcase },
  { id: 16, cardNumber: '16', title: 'طلب إجازة مرضية طويلة', desc: 'اعتماد الإجازات المرضية الطويلة بناءً على تقارير اللجنة الطبية المختصة.', type: 'military', attachmentsCount: 3, duration: '48 ساعة', target: 'الكل', icon: Activity },
  { id: 17, cardNumber: '17', title: 'طلب انتداب مؤقت لخارج القوة', desc: 'انتداب الفرد للعمل لدى جهة أو إدارة أخرى مؤقتاً مع تنظيم صرف مستحقاته المالية.', type: 'military', attachmentsCount: 3, duration: '72 ساعة', target: 'ضباط فقط', icon: ExternalLink },
  { id: 18, cardNumber: '18', title: 'طلب إنهاء انتداب وعودة للخدمة', desc: 'إنهاء فترة الانتداب وإعادة الفرد لجهته الأصلية وتحديث موقعه بقاعدة البيانات.', type: 'military', attachmentsCount: 2, duration: '24 ساعة', target: 'الكل', icon: Reply },
  { id: 19, cardNumber: '19', title: 'طلب صرف بدل تمثال خارجي', desc: 'مخصص مالي للضباط الموفدين في مهام رسمية أو دورات تدريبية خارج الدولة.', type: 'financial', attachmentsCount: 3, duration: '48 ساعة', target: 'ضباط فقط', icon: Globe },
  { id: 20, cardNumber: '20', title: 'طلب تعديل البدلات العائلية', desc: 'تحديث بيانات الحالة الاجتماعية والتابعين لاحتساب البدلات العائلية المقرة باللوائح.', type: 'financial', attachmentsCount: 2, duration: '24 ساعة', target: 'أفراد فقط', icon: Users },
  { id: 21, cardNumber: '21', title: 'تسوية فروقات مالية بأثر رجعي', desc: 'صرف مستحقات مالية متأخرة ناتجة عن تأخر تطبيق قرار ترقية أو تسوية بالمديرية.', type: 'financial', attachmentsCount: 3, duration: '72 ساعة', target: 'الكل', icon: Coins },
  { id: 22, cardNumber: '22', title: 'طلب شهادة بيان خدمة رسمية', desc: 'إصدار وثيقة رسمية توضح التسلسل المهني والوظائف التي شغلها المنتسب خلال خدمته.', type: 'military', attachmentsCount: 1, duration: '12 ساعة', target: 'الكل', icon: FileText },
  { id: 23, cardNumber: '23', title: 'طلب كف يد مؤقت عن العمل', desc: 'إيقاف الفرد مؤقتاً عن ممارسة مهامه وصرف نصف راتبه لوقوعه تحت ذمة التحقيق الجاري.', type: 'disciplinary', attachmentsCount: 2, duration: '12 ساعة', target: 'الكل', icon: FileX },
  { id: 24, cardNumber: '24', title: 'إعادة للخدمة وتسوية المستحقات', desc: 'تسوية الوضع المهني والمالي للفرد وإعادة كامل مستحقاته بعد صدور حكم البراءة النهائي.', type: 'disciplinary', attachmentsCount: 4, duration: '48 ساعة', target: 'الكل', icon: UserPlus }
])

const filteredCards = computed(() => {
  return serviceCards.value.filter(card => {
    const matchesCat = selectedCategory.value === 'all' || card.type === selectedCategory.value
    const matchesQuery = !searchQuery.value || 
                         card.title.includes(searchQuery.value) || 
                         card.desc.includes(searchQuery.value) || 
                         card.cardNumber.includes(searchQuery.value)
    return matchesCat && matchesQuery
  })
})

const stats = computed(() => {
  const allCount = serviceCards.value.length
  const militaryCount = serviceCards.value.filter(c => c.type === 'military').length
  const financialCount = serviceCards.value.filter(c => c.type === 'financial').length
  const disciplinaryCount = serviceCards.value.filter(c => c.type === 'disciplinary').length

  return [
    {
      label: 'إجمالي كروت الخدمة',
      value: `${allCount} كرت خدمة`,
      icon: LayoutGrid,
      colorClass: 'bg-brand-500/10 text-brand-650 border-brand-500/20 dark:bg-brand-500/5 dark:text-brand-400 dark:border-brand-500/10'
    },
    {
      label: 'حركات الأفراد والتعيينات',
      value: `${militaryCount} كروت حركية`,
      icon: Users,
      colorClass: 'bg-blue-500/10 text-blue-600 border-blue-500/20 dark:bg-blue-500/5 dark:text-blue-400 dark:border-blue-500/10'
    },
    {
      label: 'الخدمات المالية والرواتب',
      value: `${financialCount} خدمات مالية`,
      icon: Coins,
      colorClass: 'bg-emerald-500/10 text-emerald-600 border-emerald-500/20 dark:bg-emerald-500/5 dark:text-emerald-400 dark:border-emerald-500/10'
    },
    {
      label: 'شؤون الانضباط والإجراءات',
      value: `${disciplinaryCount} قرارات انضباطية`,
      icon: ShieldAlert,
      colorClass: 'bg-rose-500/10 text-rose-600 border-rose-500/20 dark:bg-rose-500/5 dark:text-rose-400 dark:border-rose-500/10'
    }
  ]
})
</script>
