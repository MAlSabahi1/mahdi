<template>
  <div class="flex flex-col w-full">
    <!-- Node Row -->
    <div 
      @click="toggle"
      class="grid grid-cols-12 gap-4 px-6 py-3 border-b border-gray-100 dark:border-gray-700/50 hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors cursor-pointer select-none"
      :class="{ 'bg-gray-50/50 dark:bg-gray-700/20': expanded }"
    >
      <div class="col-span-8 flex items-center gap-2">
        <!-- Indentation spacer -->
        <div :style="{ width: `${level * 24}px` }" class="flex-shrink-0"></div>
        
        <!-- Expand/Collapse Icon -->
        <div v-if="hasChildren" class="w-6 h-6 flex items-center justify-center text-gray-400">
          <svg v-if="expanded" class="w-4 h-4 transform text-gray-600 dark:text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          <svg v-else class="w-4 h-4 transform -rotate-90 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
        </div>
        <div v-else class="w-6 h-6 flex items-center justify-center text-gray-300">
          <div class="w-1.5 h-1.5 rounded-full bg-gray-300 dark:bg-gray-600"></div>
        </div>
        
        <!-- Node Name & Type Icon -->
        <span class="font-bold flex items-center gap-2" :class="nameColorClass">
          <svg v-if="node.type === 'sa'" class="w-5 h-5 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
          <svg v-else-if="node.type === 'l1'" class="w-5 h-5 text-teal-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"></path></svg>
          <svg v-else-if="node.type === 'div'" class="w-4 h-4 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
          <svg v-else class="w-4 h-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
          {{ node.name }}
        </span>
      </div>

      <!-- Counts -->
      <div class="col-span-1 flex items-center justify-center font-bold text-blue-600 dark:text-blue-400">{{ node.officers }}</div>
      <div class="col-span-1 flex items-center justify-center font-bold text-emerald-600 dark:text-emerald-400">{{ node.ncos }}</div>
      <div class="col-span-2 flex items-center justify-center">
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-indigo-100 text-indigo-800 dark:bg-indigo-900/50 dark:text-indigo-300">
          {{ node.total }}
        </span>
      </div>
    </div>

    <!-- Children -->
    <div v-show="expanded && hasChildren" class="flex flex-col w-full border-r-2 border-gray-100 dark:border-gray-700/50 ml-2 print:border-r-0 print:!flex">
      <TreeNode 
        v-for="(child, idx) in node.children" 
        :key="idx" 
        :node="child" 
        :level="level + 1" 
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, inject } from 'vue'

const props = defineProps<{
  node: any
  level: number
}>()

const expanded = ref(props.level < 2) // Auto expand first two levels

const hasChildren = computed(() => {
  return props.node.children && props.node.children.length > 0
})

const toggle = () => {
  if (hasChildren.value) {
    expanded.value = !expanded.value
  }
}

const nameColorClass = computed(() => {
  if (props.node.type === 'sa') return 'text-red-700 dark:text-red-400 text-lg'
  if (props.node.type === 'l1') return 'text-teal-700 dark:text-teal-400 text-base'
  if (props.node.type === 'div') return 'text-blue-700 dark:text-blue-400 text-sm'
  return 'text-gray-700 dark:text-gray-300 text-sm'
})
</script>
<script lang="ts">
export default {
  name: 'TreeNode' // required for recursive components
}
</script>
