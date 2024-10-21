<template>
  <div class="space-y-3">
    <h3 class="text-2xl font-semibold font-sans text-primary-800">Insights</h3>
    <Card v-if="applications.data" class="max-w-[320px] !shadow-none border">
      <template #title>{{ applications.data.length }}</template>
      <template #subtitle>
        <span class="text-sm font-medium uppercase text-primary-600">
          Total Submissions
        </span>
      </template>
    </Card>
    <div v-if="applications.loading">
      <LoadingText />
    </div>
    <div
      v-if="applications.data?.length == 0"
      class="flex justify-center items-center bg-primary-50 p-4 min-h-28 rounded border-2 border-dashed border-primary-300"
    >
      <h4 class="text-base text-primary-700 font-medium">
        No Submissions Yet.
      </h4>
    </div>
    <div v-else>
      <DataTable :value="applications.data">
        <template #header>
          <span class="text-lg font-semibold font-sans text-primary-800">
            Submissions
          </span>
        </template>
        <Column
          v-for="c in columns"
          :key="c.field"
          :field="c.field"
          :header="c.header"
        >
        </Column>
      </DataTable>
    </div>
  </div>
</template>
<script setup>
import { createResource, LoadingText } from 'frappe-ui'
import { useRoute } from 'vue-router'
import Card from 'primevue/card'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { ref } from 'vue'

const route = useRoute()

const props = defineProps({
  nominationForm: {
    type: Object,
    required: true,
  },
})

const applications = createResource({
  url: 'frappe.client.get_list',
  makeParams() {
    return {
      doctype: 'Election Candidate Application',
      fields: ['status', 'full_name', 'photo', 'name'],
      filters: {
        election: route.params.id,
      },
      limit_page_length: 999,
    }
  },
  auto: true,
})

const columns = ref([
  { field: 'name', header: 'ID' },
  { field: 'full_name', header: 'Name' },
  { field: 'status', header: 'Status' },
])
</script>
