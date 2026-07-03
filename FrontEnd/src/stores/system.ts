import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface System {
  id: string
  nameKey: string
  icon: string
}

export const useSystemStore = defineStore('system', () => {
  // Get active system from localStorage or default to 'administration'
  const currentSystem = ref<string>(localStorage.getItem('pol_active_system') || 'administration')

  // Define the 4 core systems with their i18n keys and icons
  const systems = ref<System[]>([
    {
      id: 'administration',
      nameKey: 'systems.administration',
      icon: 'LayoutDashboardIcon'
    },
    {
      id: 'secretariat',
      nameKey: 'systems.secretariat',
      icon: 'DocsIcon'
    },
    {
      id: 'services_personnel',
      nameKey: 'systems.services_personnel',
      icon: 'UserGroupIcon'
    },
    {
      id: 'users_permissions',
      nameKey: 'systems.users_permissions',
      icon: 'SettingsIcon'
    }
  ])

  // Change the active system and save it
  function switchSystem(systemId: string) {
    currentSystem.value = systemId
    localStorage.setItem('pol_active_system', systemId)
  }

  return {
    currentSystem,
    systems,
    switchSystem
  }
})
