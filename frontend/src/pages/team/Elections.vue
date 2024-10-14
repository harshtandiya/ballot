<template>
  <div class="p-4 flex flex-col gap-4">
    <div class="space-y-2">
      <h1 class="text-3xl font-semibold font-sans">Elections</h1>
      <p class="text-base text-primary-700">
        Create and manage elections with your team.
      </p>
      <CreateElectionDialog @reload-elections="elections.fetch()" />
    </div>
    <div>
      <div v-if="elections.list.loading" class="text-sm">Loading...</div>
      <div v-if="!elections.data || elections.data.length == 0">
        <span class="text-base text-primary-600">
          Your team hasn't created any elections yet.
        </span>
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <ElectionCard
          v-for="election in elections.data"
          :key="election.name"
          :election="election"
          @click="
            router.push({
              name: 'Election Dashboard',
              params: { id: election.name },
            })
          "
        ></ElectionCard>
      </div>
    </div>
  </div>
</template>
<script setup>
import { createListResource } from 'frappe-ui'
import { useRoute, useRouter } from 'vue-router'
import ElectionCard from '@/components/election/ElectionCard.vue'
import CreateElectionDialog from '@/components/election/CreateElectionDialog.vue'

const route = useRoute()
const router = useRouter()

const elections = createListResource({
  doctype: 'Election',
  filters: {
    organizing_team: route.params.id,
  },
  fields: ['*'],
  pageLength: 999,
  auto: true,
})
</script>
