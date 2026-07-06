<template>
  <admin-layout>
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
            <GitMerge class="w-8 h-8 text-indigo-600" />
            مُنشئ مسارات العمل (Workflow Builder)
          </h1>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            رسم مسار وتدفق الاعتمادات للخدمة: {{ service?.name_ar }}
          </p>
        </div>
        <div class="flex gap-3">
          <button @click="router.push('/services/directory')"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
            العودة للدليل
          </button>
        </div>
      </div>

      <div v-if="loading" class="flex justify-center py-20">
        <Loader2 class="w-10 h-10 animate-spin text-brand-500" />
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Left Sidebar: Available Stages -->
        <div class="lg:col-span-1 space-y-4">
          <div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">المراحل المتاحة</h2>

            <div class="space-y-3">
              <div v-for="stage in availableStages" :key="stage.id"
                class="p-3 border border-gray-200 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-900 hover:border-brand-500 cursor-pointer flex items-center justify-between group transition-colors"
                @click="addStep(stage)">
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ stage.name_ar }}</span>
                <PlusCircle class="w-5 h-5 text-gray-400 group-hover:text-brand-500" />
              </div>
            </div>

            <button @click="showAddStageModal = true"
              class="mt-4 w-full py-2 border-2 border-dashed border-gray-300 text-gray-500 rounded-lg hover:border-brand-500 hover:text-brand-500 text-sm font-medium flex justify-center items-center gap-2">
              <Plus class="w-4 h-4" /> مرحلة جديدة
            </button>
          </div>
        </div>

        <!-- Right Area: Workflow Sequence -->
        <div class="lg:col-span-3">
          <div
            class="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 min-h-[500px]">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">تسلسل سير العمل</h2>

            <div v-if="workflowSteps.length === 0" class="flex flex-col items-center justify-center py-20 text-center">
              <GitCommit class="w-16 h-16 text-gray-300 mb-4" />
              <h3 class="text-lg font-medium text-gray-900 dark:text-white">لا توجد خطوات</h3>
              <p class="text-sm text-gray-500 mt-1 max-w-sm">
                لم يتم تعريف أي مسار لهذه الخدمة بعد. قم بإضافة مراحل من القائمة الجانبية لبناء التسلسل.
              </p>
            </div>

            <div v-else
              class="space-y-4 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-gray-300 before:to-transparent">

              <div v-for="(step, index) in workflowSteps" :key="index"
                class="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">

                <div
                  class="flex items-center justify-center w-10 h-10 rounded-full border-4 border-white dark:border-gray-900 bg-brand-500 text-white shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow-sm relative z-10 font-bold text-sm">
                  {{ index + 1 }}
                </div>

                <div
                  class="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 p-4 rounded-xl shadow-sm relative">
                  <button @click="removeStep(index)"
                    class="absolute top-3 left-3 p-1 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded">
                    <Trash2 class="w-4 h-4" />
                  </button>

                  <h3 class="font-bold text-gray-900 dark:text-white">{{ step.stage_details?.name_ar ||
                    getStageName(step.stage) }}</h3>

                  <div class="mt-4 space-y-3">
                    <div>
                      <label class="text-xs text-gray-500 block mb-1">وصف الخطوة (تعليمات للموظف)</label>
                      <input type="text" v-model="step.description"
                        class="w-full text-sm p-2 border border-gray-200 rounded-lg dark:bg-gray-900 dark:border-gray-700 outline-none focus:border-brand-500"
                        placeholder="مثال: مراجعة المستندات والتأكد من مطابقتها" />
                    </div>

                    <div class="flex flex-wrap gap-4 pt-2">
                      <label class="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                        <input type="checkbox" v-model="step.requires_approval"
                          class="rounded text-brand-600 focus:ring-brand-500">
                        تتطلب اعتماد
                      </label>

                      <label class="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                        <input type="checkbox" v-model="step.is_execution_step"
                          class="rounded text-brand-600 focus:ring-brand-500">
                        خطوة تنفيذ / إصدار
                      </label>

                      <label class="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                        <input type="checkbox" v-model="step.is_final_step" @change="ensureOnlyOneFinal(index)"
                          class="rounded text-brand-600 focus:ring-brand-500">
                        خطوة نهائية (موافقة عامة)
                      </label>
                    </div>
                  </div>
                </div>
              </div>

            </div>

            <div class="mt-10 pt-6 border-t border-gray-200 dark:border-gray-700 flex justify-end">
              <button @click="saveWorkflow" :disabled="saving"
                class="px-6 py-2.5 text-sm font-medium text-white bg-indigo-600 rounded-xl hover:bg-indigo-700 disabled:opacity-50 flex items-center gap-2 shadow-sm">
                <Save v-if="!saving" class="w-4 h-4" />
                <Loader2 v-else class="w-4 h-4 animate-spin" />
                حفظ مسار العمل والتسلسل
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { useRouter, useRoute } from 'vue-router'
import { GitMerge, Save, Loader2, Plus, PlusCircle, GitCommit, Trash2 } from 'lucide-vue-next'
import Swal from 'sweetalert2'
import api from '@/lib/api'

const router = useRouter()
const route = useRoute()
const serviceId = route.query.id as string

const loading = ref(true)
const saving = ref(false)
const service = ref<any>(null)
const availableStages = ref<any[]>([])
const workflowSteps = ref<any[]>([])
const showAddStageModal = ref(false) // placeholder for modal

onMounted(async () => {
  if (!serviceId) {
    Swal.fire({ icon: 'error', text: 'رقم الخدمة مفقود' })
    router.push('/services/directory')
    return
  }

  try {
    // Fetch service info
    const sRes = await api.get(`/service-cycle/catalog/${serviceId}/`)
    service.value = sRes.data

    // Fetch available stages
    const stRes = await api.get('/service-cycle/workflow-stages/')
    availableStages.value = stRes.data.results || stRes.data

    // Fetch existing steps
    const wRes = await api.get(`/service-cycle/workflow-steps/?service_id=${serviceId}`)
    workflowSteps.value = (wRes.data.results || wRes.data).sort((a: any, b: any) => a.order - b.order)

  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})

function getStageName(stageId: number) {
  const st = availableStages.value.find(s => s.id === stageId)
  return st ? st.name_ar : 'مرحلة'
}

function addStep(stage: any) {
  workflowSteps.value.push({
    service: parseInt(serviceId),
    stage: stage.id,
    stage_details: stage,
    order: workflowSteps.value.length + 1,
    description: `مراجعة ${stage.name_ar}`,
    is_final_step: false,
    is_execution_step: false,
    requires_approval: true
  })
}

function removeStep(index: number) {
  workflowSteps.value.splice(index, 1)
  // Reorder
  workflowSteps.value.forEach((step, idx) => {
    step.order = idx + 1
  })
}

function ensureOnlyOneFinal(index: number) {
  if (workflowSteps.value[index].is_final_step) {
    workflowSteps.value.forEach((step, idx) => {
      if (idx !== index) step.is_final_step = false
    })
  }
}

async function saveWorkflow() {
  saving.value = true
  try {
    const payload = {
      service_id: parseInt(serviceId),
      steps: workflowSteps.value.map((step, i) => ({
        stage: step.stage,
        order: step.order || i + 1,
        description: step.description,
        is_final_step: step.is_final_step,
        is_execution_step: step.is_execution_step,
        requires_approval: step.requires_approval
      }))
    }
    
    await api.post('/service-cycle/workflow-steps/bulk-sync/', payload)

    Swal.fire({ icon: 'success', title: 'تم الحفظ', text: 'تم حفظ مسار العمل بنجاح', timer: 1500, showConfirmButton: false })
  } catch (err) {
    console.error(err)
    Swal.fire({ icon: 'error', title: 'خطأ', text: 'فشل حفظ المسار' })
  } finally {
    saving.value = false
  }
}
</script>
