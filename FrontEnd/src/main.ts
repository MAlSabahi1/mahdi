import './assets/main.css'
// Import Swiper styles
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'
import 'jsvectormap/dist/jsvectormap.css'
import 'flatpickr/dist/flatpickr.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import VueApexCharts from 'vue3-apexcharts'
import { useAuthStore } from './stores/auth'
import i18n from './i18n'
import { fieldError } from './directives/fieldError'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(i18n)
app.use(VueApexCharts)
app.directive('field-error', fieldError)

// Initialize auth state from localStorage
const authStore = useAuthStore()
authStore.initFromStorage()

app.mount('#app')
