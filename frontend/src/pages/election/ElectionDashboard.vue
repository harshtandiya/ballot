<template>
  <div class="flex">
    <Sidebar :sidebar-items="sidebarItems">
      <template #pre-nav-items>
        <div>
          <Button
            v-if="election.data"
            label="Go Back"
            icon-left="arrow-left"
            variant="ghost"
            :route="`/my-team/${election.data.organizing_team}/elections`"
          />
        </div>
        <div>
          <h4 class="text-sm uppercase mb-0 font-semibold">Manage Election</h4>
          <hr class="my-2" />
          <span v-if="election.data" class="text-base">{{
            election.data.title
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
import Sidebar from '@/components/Sidebar.vue'
import { useRoute } from 'vue-router'
import { createResource } from 'frappe-ui'

const route = useRoute()

const election = createResource({
  url: 'frappe.client.get',
  makeParams() {
    return {
      doctype: 'Election',
      name: route.params.id,
    }
  },
  auto: true,
})

const sidebarItems = [
  {
    label: 'Details',
    route: `/my-elections/${route.params.id}`,
  },
  {
    label: 'Manage Candidates',
    route: `/my-elections/${route.params.id}/nomination`,
  },
]
</script>
