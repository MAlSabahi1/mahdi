import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'

export type AppLang = 'ar' | 'en'

export const useLangStore = defineStore('lang', () => {
  // Default to Arabic
  const currentLang = ref<AppLang>((localStorage.getItem('app_lang') as AppLang) || 'ar')

  // Set the HTML direction and lang attribute based on current language
  const applyHtmlAttributes = (lang: AppLang) => {
    const htmlEl = document.documentElement
    htmlEl.setAttribute('lang', lang)
    htmlEl.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr')
  }

  // Set language function
  const setLanguage = (lang: AppLang) => {
    currentLang.value = lang
    localStorage.setItem('app_lang', lang)
    applyHtmlAttributes(lang)
  }

  // Initial setup
  applyHtmlAttributes(currentLang.value)

  return {
    currentLang,
    setLanguage
  }
})
