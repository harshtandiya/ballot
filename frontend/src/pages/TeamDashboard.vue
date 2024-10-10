<template>
  <div class="flex">
    <Sidebar :sidebar-items="sidebarItems" />
    <div class="w-full md:ml-[220px]">
      <RouterView />
    </div>
  </div>
</template>
<script setup>
import { createDocumentResource, createResource } from 'frappe-ui'
import { useRoute } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import { provide } from 'vue'

const route = useRoute()

const team = createDocumentResource({
  doctype: 'Election Team',
  name: route.params.id,
  auto: true,
})

provide('$team', team.doc)

const sidebarItems = [
  {
    label: 'Details',
    route: `/myteam/${route.params.id}`,
  },
]
</script>
