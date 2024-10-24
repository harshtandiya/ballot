<template>
  <router-link :to="submission.route">
    <Card
      class="!shadow-none border border-primary-200 hover:border-primary-500 hover:cursor-pointer transition-colors ease-in-out"
    >
      <template #content>
        <div class="flex flex-col gap-2">
          <h5 class="text-base font-medium">{{ submission.election_title }}</h5>
          <Tag
            :value="submission.status"
            class="w-fit !text-sm !font-medium"
            :severity="
              { Pending: 'warn', Accepted: 'success', Rejected: 'danger' }[
                submission.status
              ]
            "
          ></Tag>
          <span class="text-sm"
            >Submitted on
            {{ dayjs(submission.creation).format('DD MMM YYYY') }}</span
          >
        </div>
      </template>
    </Card>
  </router-link>
</template>
<script setup>
import Tag from 'primevue/tag'
import Card from 'primevue/card'
import dayjs from 'dayjs'
defineProps({
  submission: {
    type: Object,
    required: true,
  },
})
</script>
