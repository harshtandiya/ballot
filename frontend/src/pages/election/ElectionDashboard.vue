<template>
  <div class="flex">
    <Sidebar :sidebar-items="sidebarItems" />
    <div class="w-full md:ml-[220px]">
      <RouterView />
    </div>
  </div>
</template>
<script setup>
import Sidebar from '@/components/Sidebar.vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const sidebarItems = [
  {
    label: 'Details',
    route: `/my-elections/${route.params.id}`,
  },
  {
    label: 'Nominations',
    route: `/my-elections/${route.params.id}/nomination`,
  },
]
</script>
