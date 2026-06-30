<template>
  <button
    @click="toggleLanguage"
    class="flex items-center justify-center w-10 h-10 text-gray-700 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800 rounded-lg transition-colors"
    :title="currentLang === 'ar' ? 'Switch to English' : 'التبديل للعربية'"
  >
    <span class="text-sm font-semibold uppercase">{{ currentLang === 'ar' ? 'EN' : 'ع' }}</span>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useLangStore } from '@/stores/lang'
import { useI18n } from 'vue-i18n'

const langStore = useLangStore()
const { locale } = useI18n()

const currentLang = computed(() => langStore.currentLang)

const toggleLanguage = () => {
  const newLang = currentLang.value === 'ar' ? 'en' : 'ar'
  langStore.setLanguage(newLang)
  locale.value = newLang
}
</script>
