import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/lib/api'

export interface CoreReferenceItem {
  id: number
  name: string
  code?: string
  [key: string]: any
}

export const useCoreStore = defineStore('core', () => {
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Reference Data State
  const ranks = ref<CoreReferenceItem[]>([])
  const statuses = ref<CoreReferenceItem[]>([])
  const securityAdmins = ref<CoreReferenceItem[]>([])
  const centralDepartments = ref<CoreReferenceItem[]>([])
  const branches = ref<CoreReferenceItem[]>([])
  const districtPolices = ref<CoreReferenceItem[]>([])
  const divisions = ref<CoreReferenceItem[]>([])
  const units = ref<CoreReferenceItem[]>([])
  
  const jobCategories = ref<CoreReferenceItem[]>([])
  const jobTitles = ref<CoreReferenceItem[]>([])
  const positions = ref<CoreReferenceItem[]>([])
  const forceTypes = ref<CoreReferenceItem[]>([])
  const qualifications = ref<CoreReferenceItem[]>([])
  const governorates = ref<CoreReferenceItem[]>([])

  async function fetchAllReferences() {
    loading.value = true
    error.value = null
    try {
      // Use Promise.all for concurrent fetching
      const [
        ranksRes, statusesRes, adminsRes, deptsRes,
        branchesRes, districtsRes, divisionsRes, unitsRes,
        categoriesRes, titlesRes, positionsRes, forcesRes,
        qualsRes, govsRes
      ] = await Promise.all([
        api.get('/dictionaries/ranks/'),
        api.get('/dictionaries/statuses/'),
        api.get('/dictionaries/security-admins/'),
        api.get('/dictionaries/central-departments/'),
        api.get('/dictionaries/branches/'),
        api.get('/dictionaries/district-police/'),
        api.get('/dictionaries/divisions/'),
        api.get('/dictionaries/units/'),
        api.get('/dictionaries/job-categories/'),
        api.get('/dictionaries/job-titles/'),
        api.get('/dictionaries/positions/'),
        api.get('/dictionaries/force-types/'),
        api.get('/dictionaries/qualifications/'),
        api.get('/dictionaries/geo/governorates/'),
      ])

      ranks.value = ranksRes.data.results || ranksRes.data
      statuses.value = statusesRes.data.results || statusesRes.data
      securityAdmins.value = adminsRes.data.results || adminsRes.data
      centralDepartments.value = deptsRes.data.results || deptsRes.data
      branches.value = branchesRes.data.results || branchesRes.data
      districtPolices.value = districtsRes.data.results || districtsRes.data
      divisions.value = divisionsRes.data.results || divisionsRes.data
      units.value = unitsRes.data.results || unitsRes.data
      jobCategories.value = categoriesRes.data.results || categoriesRes.data
      jobTitles.value = titlesRes.data.results || titlesRes.data
      positions.value = positionsRes.data.results || positionsRes.data
      forceTypes.value = forcesRes.data.results || forcesRes.data
      qualifications.value = qualsRes.data.results || qualsRes.data
      // Note: Geo models have name_ar instead of name
      governorates.value = (govsRes.data.results || govsRes.data).map((g: any) => ({
        id: g.id,
        name: g.name_ar,
      }))
    } catch (err: any) {
      console.error('Failed to fetch core references:', err)
      error.value = 'فشل جلب البيانات المرجعية الأساسية'
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    ranks,
    statuses,
    securityAdmins,
    centralDepartments,
    branches,
    districtPolices,
    divisions,
    units,
    jobCategories,
    jobTitles,
    positions,
    forceTypes,
    qualifications,
    governorates,
    fetchAllReferences,
  }
})
