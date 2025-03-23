<template>
  <div
    class="flex gap-3 grow items-start bg-white p-3 rounded border border-gray-400"
  >
    <Avatar
      v-if="candidate.photo"
      class="border rounded-sm"
      :image="candidate.photo"
    />
    <Avatar v-else :label="candidate.full_name.charAt(0)" />
    <div class="flex flex-col gap-1">
      <h5 class="text-lg font-medium">
        {{ candidate.full_name }}
      </h5>
      <div class="text-sm">
        {{ candidate.designation }} at
        {{ candidate.organization }}
      </div>
      <a
        :href="`/ballot/election/${$route.params.slug}/c/${candidate.name}`"
        class="text-sm text-primary-600 underline flex gap-1 mt-2 self-end"
        target="_blank"
      >
        View Candidate Page
        <IconChevronRight class="text-primary-600" size="1rem" />
      </a>
    </div>
  </div>
</template>
<script setup>
import { IconChevronRight } from '@tabler/icons-vue'
import Avatar from 'primevue/avatar'
defineProps({
  candidate: {
    type: Object,
    required: true,
  },
})
</script>
