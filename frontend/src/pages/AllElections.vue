<template>
  <div class="p-4 flex flex-col gap-6">
    <div class="space-y-2 border-b pb-4">
      <h1 class="text-3xl font-semibold font-sans">All Elections</h1>
      <p class="text-base text-primary-700">List of all ongoing elections.</p>
    </div>
    <div>
      <h3 class="text-lg font-medium font-sans">Ongoing Elections</h3>
      <div v-if="liveElections.loading">
        <LoadingText />
      </div>
      <div
        v-else-if="liveElections.data.length"
        class="grid grid-cols-1 md:grid-cols-3 gap-3 my-3"
      >
        <ElectionCard
          v-for="(election, index) in liveElections.data"
          :key="index"
          :election="election"
        />
      </div>
      <div v-else>
        <p class="text-base mt-2 text-primary-500">
          There are no live elections at the moment.
        </p>
      </div>
    </div>
    <div>
      <h3 class="text-lg font-medium font-sans">Past Elections</h3>
      <div v-if="pastElections.loading">
        <LoadingText />
      </div>
      <div
        v-else-if="pastElections.data.length"
        class="grid grid-cols-1 md:grid-cols-3 gap-3 my-3"
      >
        <ElectionCard
          v-for="(election, index) in pastElections.data"
          :key="index"
          :election="election"
        />
      </div>
      <div v-else>
        <p class="text-base mt-2 text-primary-500">
          There are no past elections.
        </p>
      </div>
    </div>
  </div>
</template>
<script setup>
import { createResource, LoadingText } from 'frappe-ui'
import ElectionCard from '@/components/election/ElectionCard.vue'
import Elections from './team/Elections.vue'

const liveElections = createResource({
  url: 'frappe.client.get_list',
  makeParams() {
    return {
      doctype: 'Election',
      fields: ['title', 'status', 'creation'],
      limit_page_length: 99,
      filters: {
        status: 'Live',
      },
    }
  },
  auto: true,
})

const pastElections = createResource({
  url: 'frappe.client.get_list',
  makeParams() {
    return {
      doctype: 'Election',
      fields: ['title', 'status', 'creation'],
      limit_page_length: 99,
      filters: {
        status: 'Concluded',
      },
    }
  },
  auto: true,
})
</script>
