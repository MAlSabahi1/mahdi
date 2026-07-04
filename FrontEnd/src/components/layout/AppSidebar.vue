<template>
  <aside :class="[
    'fixed mt-16 flex flex-col lg:mt-0 top-0 px-5 start-0 bg-white dark:bg-gray-900 dark:border-gray-800 text-gray-900 h-screen transition-all duration-300 ease-in-out z-99999 border-e border-gray-200',
    {
      'lg:w-[290px]': isExpanded || isMobileOpen || isHovered,
      'lg:w-[90px]': !isExpanded && !isHovered,
      'translate-x-0 w-[290px]': isMobileOpen,
      'max-lg:-translate-x-full rtl:max-lg:translate-x-full': !isMobileOpen,
      'lg:translate-x-0': true,
    },
  ]" @mouseenter="!isExpanded && (isHovered = true)" @mouseleave="isHovered = false">
    <div :class="[
      'py-6 flex items-center justify-center border-b border-gray-100 dark:border-gray-800 mb-6 -mx-5 px-5',
    ]">
      <router-link to="/">
        <img v-if="isExpanded || isHovered || isMobileOpen" src="/images/logo/logoBase.svg" alt="Logo" class="h-10 md:h-14 w-auto max-w-[220px]" />
        <img v-else src="/images/logo/logoBase.svg" alt="Logo" class="h-10 w-10 md:h-12 md:w-12 object-contain" />
      </router-link>
    </div>
    <div class="flex flex-col overflow-y-auto duration-300 ease-linear no-scrollbar">
      <nav class="mb-6">
        <div class="flex flex-col gap-4">
          <div v-for="(menuGroup, groupIndex) in menuGroups" :key="groupIndex">
            <h2 :class="[
              'mb-4 text-xs uppercase flex leading-[20px] text-gray-400',
              !isExpanded && !isHovered
                ? 'lg:justify-center'
                : 'justify-start',
            ]">
              <template v-if="isExpanded || isHovered || isMobileOpen">
                {{ $t(menuGroup.title) }}
              </template>
              <HorizontalDots v-else />
            </h2>
            <ul class="flex flex-col gap-4">
              <li v-for="(item, index) in menuGroup.items" :key="item.name">
                <button v-if="item.subItems" @click="toggleSubmenu(groupIndex, index)" :class="[
                  'menu-item group w-full',
                  {
                    'menu-item-active': isSubmenuOpen(groupIndex, index),
                    'menu-item-inactive': !isSubmenuOpen(groupIndex, index),
                  },
                  !isExpanded && !isHovered
                    ? 'lg:justify-center'
                    : 'lg:justify-start',
                ]">
                  <span :class="[
                    isSubmenuOpen(groupIndex, index)
                      ? 'menu-item-icon-active'
                      : 'menu-item-icon-inactive',
                  ]">
                    <component :is="item.icon" />
                  </span>
                  <span v-if="isExpanded || isHovered || isMobileOpen" class="menu-item-text text-start flex-1">{{ $t(item.name) }}</span>
                  <ChevronDownIcon v-if="isExpanded || isHovered || isMobileOpen" :class="[
                    'ms-auto w-5 h-5 transition-transform duration-200',
                    {
                      'rotate-180 text-brand-500': isSubmenuOpen(
                        groupIndex,
                        index
                      ),
                    },
                  ]" />
                </button>
                <router-link v-else-if="item.path" :to="item.path" :class="[
                  'menu-item group',
                  {
                    'menu-item-active': isActive(item.path),
                    'menu-item-inactive': !isActive(item.path),
                  },
                ]">
                  <span :class="[
                    isActive(item.path)
                      ? 'menu-item-icon-active'
                      : 'menu-item-icon-inactive',
                  ]">
                    <component :is="item.icon" />
                  </span>
                  <span v-if="isExpanded || isHovered || isMobileOpen" class="menu-item-text text-start flex-1">{{ $t(item.name) }}</span>
                </router-link>
                <transition @enter="startTransition" @after-enter="endTransition" @before-leave="startTransition"
                  @after-leave="endTransition">
                  <div v-show="isSubmenuOpen(groupIndex, index) &&
                    (isExpanded || isHovered || isMobileOpen)
                    ">
                    <ul class="mt-2 space-y-1 ms-9">
                      <li v-for="subItem in item.subItems" :key="subItem.name">
                        <router-link :to="subItem.path" :class="[
                          'menu-dropdown-item',
                          {
                            'menu-dropdown-item-active': isActive(
                              subItem.path
                            ),
                            'menu-dropdown-item-inactive': !isActive(
                              subItem.path
                            ),
                          },
                        ]">
                          {{ $t(subItem.name) }}
                          <span class="flex items-center gap-1 ms-auto">
                            <span v-if="subItem.new" :class="[
                              'menu-dropdown-badge',
                              {
                                'menu-dropdown-badge-active': isActive(
                                  subItem.path
                                ),
                                'menu-dropdown-badge-inactive': !isActive(
                                  subItem.path
                                ),
                              },
                            ]">
                              new
                            </span>
                            <span v-if="subItem.pro" :class="[
                              'menu-dropdown-badge',
                              {
                                'menu-dropdown-badge-active': isActive(
                                  subItem.path
                                ),
                                'menu-dropdown-badge-inactive': !isActive(
                                  subItem.path
                                ),
                              },
                            ]">
                              pro
                            </span>
                          </span>
                        </router-link>
                      </li>
                    </ul>
                  </div>
                </transition>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
    <!-- Logout Button -->
    <div
      v-if="isExpanded || isHovered || isMobileOpen"
      class="mt-auto border-t border-gray-200 px-2 py-4 dark:border-gray-800"
    >
      <button
        @click="handleLogout"
        class="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-gray-600 transition-colors hover:bg-gray-100 hover:text-gray-800 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-gray-200"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd" />
        </svg>
        {{ $t('nav.logout') }}
      </button>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import {
  GridIcon,
  ChevronDownIcon,
  HorizontalDots,
  PageIcon,
  PlugInIcon,
  UserCircleIcon,
  UserGroupIcon,
  SettingsIcon,
} from "../../icons";
import { useSidebar } from "@/composables/useSidebar";
import { useAuthStore } from "@/stores/auth";
import { useSystemStore } from "@/stores/system";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const systemStore = useSystemStore();

const { isExpanded, isMobileOpen, isHovered, openSubmenu } = useSidebar();

const menuGroups = computed(() => {
  if (systemStore.currentSystem === "administration") {
    return [
      {
        title: "systems.administration",
        items: [
          {
            icon: GridIcon,
            name: "admin.dashboard_group",
            subItems: [
              {
                name: "admin.stats_dashboard",
                path: "/admin/dashboard/stats",
              },
              {
                name: "admin.analytics_dashboard",
                path: "/admin/dashboard/analytics",
              },
              {
                name: "admin.alerts_center",
                path: "/admin/dashboard/alerts",
              },
              {
                name: "admin.compliance_tracker",
                path: "/admin/dashboard/compliance",
              }
            ]
          },
          {
            icon: UserGroupIcon,
            name: "admin.structure_group",
            subItems: [
              {
                name: "admin.regions_config",
                path: "/admin/structure/regions",
              },
              {
                name: "admin.geo_tree",
                path: "/admin/structure/geo-tree",
              },
              {
                name: "admin.org_tree",
                path: "/admin/structure/org-tree",
              },
              {
                name: "admin.general_configs",
                path: "/admin/structure/general-configs",
              }
            ]
          },
          {
            icon: SettingsIcon,
            name: "admin.system_group",
            subItems: [
              {
                name: "admin.initial_seeding",
                path: "/admin/system/seeding",
              },
              {
                name: "admin.system_telemetry",
                path: "/admin/system/telemetry",
              }
            ]
          },
          {
            icon: PageIcon,
            name: "nav.audit_logs",
            path: "/audit",
          }
        ]
      }
    ];
  } else if (systemStore.currentSystem === "secretariat") {
    return [
      {
        title: "systems.secretariat",
        items: [
          {
            icon: GridIcon,
            name: "nav.secretariat_dashboard",
            path: "/secretariat/dashboard",
          },
          {
            icon: PageIcon,
            name: "nav.correspondences",
            path: "/secretariat/correspondences",
          },
          {
            icon: PageIcon,
            name: "nav.tasks",
            path: "/secretariat/tasks",
          }
        ]
      }
    ];
  } else if (systemStore.currentSystem === "services_personnel") {
    return [
      {
        title: "systems.services_personnel",
        items: [
          {
            icon: UserGroupIcon,
            name: "nav.personnel_management",
            subItems: [
              {
                name: "nav.personnel",
                path: "/personnel",
              },
              {
                name: "nav.corrections",
                path: "/personnel/corrections",
              },
              {
                name: "nav.rank_settlements",
                path: "/personnel/settlements",
              },
              {
                name: "nav.profile_search",
                path: "/personnel/profile-search",
              },
              {
                name: "nav.editor_react",
                path: "/services/editor-react",
              }
            ]
          },
          {
            icon: PageIcon,
            name: "nav.service_cycle",
            subItems: [
              {
                name: "nav.excel_export_config",
                path: "/services/export-config",
              },
              {
                name: "nav.excel_import_wizard",
                path: "/services/import-wizard",
              },
              {
                name: "services.staging",
                path: "/services/staging",
              },
              {
                name: "services.rejections",
                path: "/services/rejections",
              }
            ]
          },
          {
            icon: GridIcon,
            name: "nav.services_reports_module",
            subItems: [
              {
                name: "nav.monthly_exports",
                path: "/services/monthly-exports",
              },
              {
                name: "nav.official_reports",
                path: "/services/official-reports",
              }
            ]
          },
          {
            icon: PlugInIcon,
            name: "nav.transactions_management_module",
            subItems: [
              {
                name: "nav.cards_directory",
                path: "/services/directory",
              },
              {
                name: "nav.unified_request",
                path: "/services/request",
              },
              {
                name: "nav.inbox_transactions",
                path: "/services/inbox",
              },
              {
                name: "nav.workflow_tracking",
                path: "/services/workflows",
              }
            ]
          }
        ]
      }
    ];
  } else if (systemStore.currentSystem === "users_permissions") {
    return [
      {
        title: "systems.users_permissions",
        items: [
          {
            icon: UserGroupIcon,
            name: "nav.account_governance_module",
            subItems: [
              {
                name: "nav.users_manage",
                path: "/users",
              },
              {
                name: "nav.governance",
                path: "/users/governance",
              },
              {
                name: "nav.active_sessions",
                path: "/users/sessions",
              }
            ]
          },
          {
            icon: PlugInIcon,
            name: "nav.advanced_policy_module",
            subItems: [
              {
                name: "مجموعات الصلاحيات",
                path: "/roles/permission-groups",
              },
              {
                name: "الصلاحيات المباشرة",
                path: "/roles/permissions",
              },
              {
                name: "nav.roles",
                path: "/roles",
              },
              {
                name: "nav.policy_matrix",
                path: "/users/policy-matrix",
              },
              {
                name: "nav.emergency_access",
                path: "/users/emergency-access",
              },
              {
                name: "nav.dual_auth",
                path: "/users/dual-auth",
              },
              {
                name: "nav.audit_trail",
                path: "/users/audit-trail",
              },
              {
                name: "nav.policy_simulator",
                path: "/users/policy-simulator",
              }
            ]
          },
          {
            icon: SettingsIcon,
            name: "nav.settings",
            path: "/users/settings",
          }
        ]
      }
    ];
  }
  return [];
});

const handleLogout = async () => {
  await authStore.logout();
  router.push("/signin");
};

const isActive = (path) => route.path === path;

const toggleSubmenu = (groupIndex, itemIndex) => {
  const key = `${groupIndex}-${itemIndex}`;
  openSubmenu.value = openSubmenu.value === key ? null : key;
};

const isAnySubmenuRouteActive = computed(() => {
  return menuGroups.value.some((group) =>
    group.items.some(
      (item) =>
        item.subItems && item.subItems.some((subItem) => isActive(subItem.path))
    )
  );
});

const checkAndOpenSubmenu = () => {
  let foundSubmenu = false;
  menuGroups.value.forEach((group, groupIndex) => {
    group.items.forEach((item, itemIndex) => {
      if (item.subItems && item.subItems.some((subItem) => isActive(subItem.path))) {
        openSubmenu.value = `${groupIndex}-${itemIndex}`;
        foundSubmenu = true;
      }
    });
  });
  if (!foundSubmenu) {
    openSubmenu.value = null;
  }
};

onMounted(() => {
  checkAndOpenSubmenu();
});

watch(() => route.path, () => {
  checkAndOpenSubmenu();
});

watch(() => systemStore.currentSystem, () => {
  checkAndOpenSubmenu();
});

const isSubmenuOpen = (groupIndex, itemIndex) => {
  const key = `${groupIndex}-${itemIndex}`;
  return openSubmenu.value === key;
};

const startTransition = (el) => {
  el.style.height = "auto";
  const height = el.scrollHeight;
  el.style.height = "0px";
  el.offsetHeight; // force reflow
  el.style.height = height + "px";
};

const endTransition = (el) => {
  el.style.height = "";
};
</script>
