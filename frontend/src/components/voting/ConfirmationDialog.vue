<template>
  <Dialog
    v-model="show"
    :options="{
      title: 'Confirm your vote',
      icon: {
        name: 'alert-triangle',
        appearance: 'warning',
      },
      actions: [
        {
          label: 'Confirm',
          variant: 'solid',
          onClick: () => {
            emit('confirm-vote')
            show = false
          },
        },
        {
          label: 'Cancel',
          onClick: () => {
            show = false
          },
        },
      ],
    }"
  >
    <template #body-content>
      <p class="text-primary-600 text-base">
        Are you sure you want to vote for these candidate?
      </p>
      <div
        v-for="(candidate, index) in candidates"
        :key="index"
        class="border p-4 mt-4 rounded"
      >
        <h4 class="text-lg font-semibold"># {{ index + 1 }}</h4>
        <CandidatePreviewCard
          :candidate="candidate"
          class="!border-none !pb-0"
        />
      </div>
    </template>
  </Dialog>
</template>
<script setup>
import { Dialog } from 'frappe-ui'
import CandidatePreviewCard from './CandidatePreviewCard.vue'
const show = defineModel('show', { type: Boolean, required: true })
const props = defineProps({
  candidates: {
    type: Array,
    required: true,
  },
})
const emit = defineEmits(['confirm-vote'])
</script>
