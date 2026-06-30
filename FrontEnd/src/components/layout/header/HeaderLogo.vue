<template>
  <router-link to="/" class="lg:hidden">
    <img src="/images/logo/logoBase.svg" alt="Logo" class="h-8 w-auto max-w-[200px]" />
    <img class="hidden" src="/images/logo/logoBase.svg" alt="Logo" />
  </router-link>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>
