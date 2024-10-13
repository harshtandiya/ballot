<template>
  <Card
    class="!shadow-none border border-primary-200 hover:border-primary-500 hover:cursor-pointer transition-colors ease-in-out"
  >
    <template #title>{{ election.title }}</template>
    <template #content>
      <Badge :theme="getVariant" class="!rounded-sm">
        {{ election.status }}
      </Badge>
      <div class="text-sm text-primary-600 mt-2">
        <span>
          Created on {{ dayjs(election.creation).format('D MMM YYYY') }}
        </span>
      </div>
    </template>
  </Card>
</template>
<script setup>
import { Badge } from 'frappe-ui'
import Card from 'primevue/card'
import { computed } from 'vue'
import dayjs from 'dayjs'

const props = defineProps({
  election: {
    type: Object,
    required: true,
  },
})

const getVariant = computed(() => {
  switch (props.election.status) {
    case 'Draft':
      return 'blue'
    case 'Live':
      return 'green'
    case 'Cancelled':
      return 'red'
    case 'Concluded':
      return 'gray'
    default:
      return 'gray'
  }
})
</script>
