<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="دليل الخدمات والاستمارات المعتمدة (24 كرت خدمة)" />

    <div class="space-y-6 text-start" dir="rtl">
      
      <!-- Page Header -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-gray-200 dark:border-gray-800 pb-5">
        <div>
          <h1 class="text-2xl font-black text-gray-900 dark:text-white">
            دليل كروت الخدمات والاستمارات المعتمدة
          </h1>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            دليل تفصيلي يوثق كافة كروت الخدمة الـ 24 المعتمدة رسمياً في النظام لتقديم الطلبات الإدارية وحركات الأفراد والضباط.
          </p>
        </div>
        
        <div class="w-full md:w-64">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="البحث في كروت الخدمات..." 
            class="w-full text-xs border border-gray-200 dark:border-gray-800 rounded-lg p-2 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300 focus:border-brand-500"
          />
        </div>
      </div>

      <!-- Categories Tabs -->
      <div class="flex flex-wrap gap-2 border-b border-gray-150 dark:border-gray-800 pb-3">
        <button 
          v-for="cat in categories" 
          :key="cat.id" 
          @click="selectedCategory = cat.id"
          :class="[
            selectedCategory === cat.id 
              ? 'bg-brand-600 text-white' 
              : 'bg-gray-50 dark:bg-gray-900 text-gray-600 dark:text-gray-400 hover:bg-gray-100'
          ]"
          class="px-3.5 py-1.5 text-xs font-bold rounded-lg transition-colors cursor-pointer"
        >
          {{ cat.label }}
        </button>
      </div>

      <!-- Cards Grid -->
      <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <div 
          v-for="card in filteredCards" 
          :key="card.id" 
          class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-4 shadow-theme-xs flex flex-col justify-between"
        >
          <div class="space-y-2">
            <div class="flex justify-between items-start gap-2">
              <span class="text-[9px] font-bold text-gray-400 bg-gray-50 dark:bg-gray-950 px-2 py-0.5 rounded border border-gray-150 dark:border-gray-800">
                كرت #{{ card.cardNumber }}
              </span>
              <span 
                :class="[
                  card.type === 'financial' 
                    ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/20 dark:text-emerald-400' 
                    : 'bg-blue-50 text-blue-700 dark:bg-blue-950/20 dark:text-blue-400'
                ]"
                class="text-[9px] font-bold px-2 py-0.5 rounded"
              >
                {{ card.type === 'financial' ? 'مالي واستحقاق' : 'حركة وتعيين' }}
              </span>
            </div>
            
            <h3 class="text-xs font-black text-gray-950 dark:text-white line-clamp-1">{{ card.title }}</h3>
            <p class="text-[10px] text-gray-400 line-clamp-2 leading-relaxed">{{ card.desc }}</p>
          </div>

          <div class="border-t border-gray-150 dark:border-gray-850 pt-3.5 mt-4 flex items-center justify-between">
            <span class="text-[9px] text-gray-450">المرفقات المطلوبة: {{ card.attachmentsCount }}</span>
            <RouterLink 
              to="/services/request"
              class="text-[10px] font-black text-brand-650 hover:underline cursor-pointer"
            >
              تقديم طلب ←
            </RouterLink>
          </div>
        </div>
      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'

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
}

const serviceCards = ref<ServiceCard[]>([
  { id: 1, cardNumber: '01', title: 'طلب تسوية رتبة عسكرية', desc: 'معالجة تسويات الرتب وتثبيتها للأفراد والضباط بناءً على الأوامر القيادية.', type: 'military', attachmentsCount: 3 },
  { id: 2, cardNumber: '02', title: 'طلب علاوة رتبة جديدة', desc: 'تفعيل وصرف علاوة الرتبة الجديدة المترتبة على قرارات تسوية الوضع.', type: 'financial', attachmentsCount: 2 },
  { id: 3, cardNumber: '03', title: 'طلب إحالة للتقاعد المبكر', desc: 'حصر الخدمات وتسوية المبالغ المستحقة للتقاعد العسكري ورفع الملف للإدارة.', type: 'military', attachmentsCount: 4 },
  { id: 4, cardNumber: '04', title: 'طلب تجميد الراتب المؤقت', desc: 'إيقاف المعالجة المالية للفرد لغيابه أو انقطاعه عن العمل لرفع كشوف الرد.', type: 'financial', attachmentsCount: 1 },
  { id: 5, cardNumber: '05', title: 'طلب تعديل المديرية الجغرافية', desc: 'نقل المنتسب إدارياً وجغرافياً وتعديل صلاحيات النطاق والـ ABAC التابع له.', type: 'military', attachmentsCount: 2 },
  { id: 6, cardNumber: '06', title: 'إجراء جزائي مالي استثنائي', desc: 'حسم مبالغ محددة من البدلات لقاء مخالفات انضباطية موثقة.', type: 'disciplinary', attachmentsCount: 3 },
  { id: 7, cardNumber: '07', title: 'طلب بدل سكن وإقامة للمناطق النائية', desc: 'صرف بدلات إضافية مخصصة للمناطق ذات الظروف الميدانية الصعبة.', type: 'financial', attachmentsCount: 2 },
  { id: 8, cardNumber: '08', title: 'إثبات حالة فرار/غياب رسمي', desc: 'إصدار أمر إيقاف الخدمة وتحويل الملف للشؤون القانونية والمحكمة العسكرية.', type: 'disciplinary', attachmentsCount: 3 },
  { id: 9, cardNumber: '09', title: 'طلب صرف إعانة وفاة عسكرية', desc: 'معاملة سريعة لصرف الإعانات الاستثنائية لورثة المنتسب المتوفى أثناء الواجب.', type: 'financial', attachmentsCount: 5 },
  { id: 10, cardNumber: '10', title: 'طلب استثناء فني للرقم المالي', desc: 'معالجة حالات تكرار الأرقام أو الأخطاء الهيكلية الواردة بكشف المحافظة.', type: 'financial', attachmentsCount: 1 },
  { id: 11, cardNumber: '11', title: 'طلب تسوية الوضع بعد التأهيل', desc: 'تحديث المؤهل الدراسي في الملف الشخصي وإعادة احتساب الراتب والموقع.', type: 'military', attachmentsCount: 2 },
  { id: 12, cardNumber: '12', title: 'إقرار عودة من إجازة طويلة', desc: 'إعادة تفعيل صرف الراتب وإعادة الإدراج في الكشوف الجارية بعد الانقطاع المعتمد.', type: 'military', attachmentsCount: 2 },
  // Adding placeholders up to 24 approved cards
  ...Array.from({ length: 12 }, (_, i) => ({
    id: 13 + i,
    cardNumber: String(13 + i),
    title: `كرت خدمة معتمد رقم ${13 + i}`,
    desc: 'وثيقة رسمية تحدد متطلبات ومرفقات هذه الخدمة التخصصية وقواعد موافقات الباك اند المرتبطة بها.',
    type: (13 + i) % 2 === 0 ? 'financial' : 'military' as 'military' | 'financial',
    attachmentsCount: 2
  }))
])

const filteredCards = computed(() => {
  return serviceCards.value.filter(card => {
    const matchesCat = selectedCategory.value === 'all' || card.type === selectedCategory.value
    const matchesQuery = !searchQuery.value || card.title.includes(searchQuery.value) || card.desc.includes(searchQuery.value)
    return matchesCat && matchesQuery
  })
})
</script>
