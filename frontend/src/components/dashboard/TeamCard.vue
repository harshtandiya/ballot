<template>
  <Card
    class="!shadow-none border border-primary-200 hover:border-primary-500 hover:cursor-pointer transition-colors ease-in-out"
  >
    <template #title>
      {{ team.team_name }}
    </template>
    <template #content>
      <div class="flex flex-col gap-2 mt-2">
        <div>
          <div class="flex gap-1 items-center text-sm">
            <IconUsers size="1rem" />
            <span>
              {{ team.members.length }}
            </span>
          </div>
        </div>
        <small class="text-sm text-primary-600"
          >Created by {{ team.owner_name }}</small
        >
      </div>
    </template>
  </Card>
</template>
<script setup>
import Card from 'primevue/card'
import { IconUsers } from '@tabler/icons-vue'

defineProps({
  team: {
    type: Object,
    required: true,
  },
})
</script>
