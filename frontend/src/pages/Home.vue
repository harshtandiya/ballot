<template>
  <div class="flex flex-col md:flex-row">
    <Sidebar :sidebar-items="sidebarItems" />
    <div class="w-full md:ml-[220px]">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import Sidebar from '@/components/Sidebar.vue'
import { RouterView } from 'vue-router'

const sidebarItems = [
  {
    label: 'Dashboard',
    route: '/dashboard',
  },
  {
    label: 'My Submissions',
    route: '/my-submissions',
  },
  {
    label: 'All Elections',
    route: '/elections',
  },
]
</script>
