<template>
  <div class="flex">
    <Sidebar :sidebar-items="sidebarItems">
      <template #pre-nav-items>
        <div>
          <Button
            label="Go Home"
            icon-left="arrow-left"
            variant="ghost"
            :route="`/`"
          />
        </div>
        <div>
          <h4 class="text-sm uppercase mb-0 font-semibold">Manage Team</h4>
          <hr class="my-2" />
          <span v-if="team.doc" class="text-base">{{
            team.doc.team_name
          }}</span>
        </div>
      </template>
    </Sidebar>
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
