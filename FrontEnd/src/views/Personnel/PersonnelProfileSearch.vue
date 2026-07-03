<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <PageBreadcrumb pageTitle="الملف الكامل للمنتسب" />

    <div class="space-y-6 text-start max-w-4xl mx-auto" dir="rtl">
      
      <!-- Page Header -->
      <div class="border-b border-gray-200 dark:border-gray-800 pb-5 text-center">
        <h1 class="text-2xl font-black text-gray-900 dark:text-white">
          البحث والاستعلام عن الملف الكامل للمنتسب
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
          أدخل الرقم العسكري أو اسم المنتسب للوصول إلى تفاصيل ملف الخدمة، الترقيات، التسويات والمرفقات بالكامل.
        </p>
      </div>

      <!-- Search Card -->
      <div class="bg-white dark:bg-white/[0.03] border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-theme-xs space-y-4">
        <div class="flex flex-col sm:flex-row gap-3">
          <div class="flex-1 relative">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="ابحث بالاسم، الرقم العسكري، أو الرقم الوطني..." 
              class="w-full text-sm border border-gray-200 dark:border-gray-800 rounded-xl p-3 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300 focus:border-brand-500 focus:ring-1 focus:ring-brand-500 pr-10"
              @input="handleSearch"
            />
            <span class="absolute right-3.5 top-3.5 text-gray-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </span>
          </div>
        </div>

        <!-- Search Results List -->
        <div class="border-t border-gray-150 dark:border-gray-850 pt-4">
          <div v-if="loading" class="flex justify-center py-6">
            <svg class="h-8 w-8 animate-spin text-brand-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
          </div>

          <div v-else-if="results.length > 0" class="space-y-2">
            <div 
              v-for="person in results" 
              :key="person.military_number"
              @click="viewProfile(person.military_number)"
              class="flex items-center justify-between p-3 border border-gray-100 dark:border-gray-800 rounded-xl hover:bg-gray-50/50 dark:hover:bg-gray-950/20 cursor-pointer transition-all"
            >
              <div class="flex items-center gap-3">
                <div class="h-10 w-10 rounded-full bg-brand-50 dark:bg-brand-950/30 text-brand-650 dark:text-brand-400 flex items-center justify-center font-bold text-sm">
                  {{ person.full_name?.substring(0, 1) }}
                </div>
                <div>
                  <h4 class="text-xs font-black text-gray-950 dark:text-white">{{ person.full_name }}</h4>
                  <p class="text-[10px] text-gray-400 mt-0.5">
                    الرقم العسكري: {{ person.military_number }} • الرتبة: {{ person.rank_name || 'غير محدد' }}
                  </p>
                </div>
              </div>

              <span class="text-[10px] text-brand-650 font-bold hover:underline">
                عرض الملف الكامل ←
              </span>
            </div>
          </div>

          <div v-else class="text-center py-8 text-gray-400 dark:text-gray-500 text-xs">
            {{ searchQuery ? 'لم يتم العثور على نتائج تطابق معايير البحث.' : 'ابدأ بكتابة اسم المنتسب أو رقمه العسكري للبحث.' }}
          </div>
        </div>
      </div>

    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import { usePersonnelStore } from '@/stores/personnel'

const router = useRouter()
const personnelStore = usePersonnelStore()

const searchQuery = ref('')
const loading = ref(false)
const results = ref<any[]>([])

async function handleSearch() {
  if (!searchQuery.value.trim()) {
    results.value = []
    return
  }

  loading.value = true
  try {
    await personnelStore.fetchPersonnel({
      search: searchQuery.value,
      page: 1
    })
    results.value = personnelStore.records || []
  } catch (error) {
    console.error('Error searching personnel:', error)
  } finally {
    loading.value = false
  }
}

function viewProfile(militaryNumber: string) {
  router.push(`/personnel/${militaryNumber}`)
}
</script>
