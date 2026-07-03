import { createI18n } from 'vue-i18n'
import ar from './locales/ar.json'
import en from './locales/en.json'

// Create i18n instance
const i18n = createI18n({
  legacy: false, // Use Composition API
  locale: localStorage.getItem('app_lang') || 'ar', // Set default locale
  fallbackLocale: 'ar',
  messages: {
    ar,
    en
  }
})

export default i18n
