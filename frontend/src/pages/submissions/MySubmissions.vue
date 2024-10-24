<template>
  <div class="px-4 py-6 flex flex-col gap-6">
    <div>
      <h1 class="text-3xl font-sans font-bold">My Submissions</h1>
    </div>
    <div v-if="submissions.loading">
      <LoadingText />
    </div>
    <div v-if="submissions.data?.length">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
        <SubmissionCard
          v-for="submission in submissions.data"
          :key="submission.name"
          :submission="submission"
        />
      </div>
    </div>
    <p v-else class="text-sm">You have not made any submissions yet.</p>
  </div>
</template>
<script setup>
import SubmissionCard from '@/components/dashboard/SubmissionCard.vue'
import { createResource, LoadingText } from 'frappe-ui'
import { inject } from 'vue'

const session = inject('$session')

const submissions = createResource({
  url: 'ballot.api.user.get_user_submissions',
  makeParams() {
    return {
      user: session.user,
    }
  },
  auto: true,
})
</script>
