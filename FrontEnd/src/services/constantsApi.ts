import api from '@/lib/api'

export interface ConstantOption {
  id: string | number
  name: string
}

export interface DepartmentOption extends ConstantOption {
  security_admin?: string | number
}

export interface DivisionOption extends ConstantOption {
  central_department?: string | number
  branch?: string | number
  district_police?: string | number
  security_admin?: string | number
}

export interface UnitOption extends ConstantOption {
  division?: string | number
}

export interface ConstantsState {
  securityAdmins: ConstantOption[]
  centralDepartments: DepartmentOption[]
  branches: DepartmentOption[]
  districtPolice: DepartmentOption[]
  divisions: DivisionOption[]
  units: UnitOption[]
  geoDistricts: ConstantOption[]
  positions: ConstantOption[]
  ranks: ConstantOption[]
  statuses: ConstantOption[]
  qualifications: ConstantOption[]
  jobCategories: ConstantOption[]
  jobTitles: ConstantOption[]
  forceTypes: ConstantOption[]
}

export const fetchAllConstants = async (): Promise<ConstantsState> => {
  const [
    securityAdmins,
    centralDepartments,
    branches,
    districtPolice,
    divisions,
    units,
    geoDistricts,
    positions,
    ranks,
    statuses,
    qualifications,
    jobCategories,
    jobTitles,
    forceTypes
  ] = await Promise.all([
    api.get('/dictionaries/security-admins/?page_size=1000').catch(() => ({ data: { results: [] } })),
    api.get('/dictionaries/central-departments/?page_size=1000').catch(() => ({ data: { results: [] } })),
    api.get('/dictionaries/branches/?page_size=1000').catch(() => ({ data: { results: [] } })),
    api.get('/dictionaries/district-police/?page_size=1000').catch(() => ({ data: { results: [] } })),
    api.get('/dictionaries/divisions/?page_size=1000').catch(() => ({ data: { results: [] } })),
    api.get('/dictionaries/units/?page_size=1000').catch(() => ({ data: { results: [] } })),
    api.get('/dictionaries/geo/districts/?page_size=1000').catch(() => ({ data: { results: [] } })),
    api.get('/dictionaries/positions/?page_size=1000').catch(() => ({ data: { results: [] } })),
    api.get('/dictionaries/ranks/?page_size=1000').catch(() => ({ data: { results: [] } })),
    api.get('/dictionaries/statuses/?page_size=1000').catch(() => ({ data: { results: [] } })),
    api.get('/dictionaries/qualifications/?page_size=1000').catch(() => ({ data: { results: [] } })),
    api.get('/dictionaries/job-categories/?page_size=1000').catch(() => ({ data: { results: [] } })),
    api.get('/dictionaries/job-titles/?page_size=1000').catch(() => ({ data: { results: [] } })),
    api.get('/dictionaries/force-types/?page_size=1000').catch(() => ({ data: { results: [] } })),
  ])

  return {
    securityAdmins: securityAdmins.data.results || securityAdmins.data || [],
    centralDepartments: centralDepartments.data.results || centralDepartments.data || [],
    branches: branches.data.results || branches.data || [],
    districtPolice: districtPolice.data.results || districtPolice.data || [],
    divisions: divisions.data.results || divisions.data || [],
    units: units.data.results || units.data || [],
    geoDistricts: geoDistricts.data.results || geoDistricts.data || [],
    positions: positions.data.results || positions.data || [],
    ranks: ranks.data.results || ranks.data || [],
    statuses: statuses.data.results || statuses.data || [],
    qualifications: qualifications.data.results || qualifications.data || [],
    jobCategories: jobCategories.data.results || jobCategories.data || [],
    jobTitles: jobTitles.data.results || jobTitles.data || [],
    forceTypes: forceTypes.data.results || forceTypes.data || [],
  }
}
