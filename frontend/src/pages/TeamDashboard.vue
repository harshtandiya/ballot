<template>
  <div class="flex">
    <Sidebar :sidebar-items="sidebarItems" />
    <div class="w-full md:ml-[220px]">
      <RouterView />
    </div>
  </div>
</template>
<script setup>
import { createDocumentResource } from 'frappe-ui'
import { useRoute } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import { provide } from 'vue'

const route = useRoute()

const team = createDocumentResource({
  doctype: 'Election Team',
  name: route.params.id,
  auto: true,
})

provide('$team', team)

const sidebarItems = [
  {
    label: 'Details',
    route: `/my-team/${route.params.id}`,
  },
  {
    label: 'Elections',
    route: `/my-team/${route.params.id}/elections`,
  },
]
</script>
