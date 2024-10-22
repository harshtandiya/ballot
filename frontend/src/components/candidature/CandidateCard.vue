<template>
  <Card
    class="!shadow-none !border hover:border-primary-700 hover:cursor-pointer transition-colors"
    @click="
      router.push({
        name: 'Candidature Submission Public',
        params: { slug: route.params.slug, id: candidate.name },
      })
    "
  >
    <template #content>
      <div class="flex gap-3 items-start">
        <Avatar v-if="candidate.photo" :image="candidate.photo" />
        <Avatar v-else :label="candidate.full_name.charAt(0)" shape="" />
        <div class="flex flex-col gap-1">
          <h5 class="text-lg font-medium">{{ candidate.full_name }}</h5>
          <div class="text-sm">
            {{ candidate.designation }} at {{ candidate.organization }}
          </div>
        </div>
      </div>
    </template>
  </Card>
</template>
<script setup>
import Card from 'primevue/card'
import Avatar from 'primevue/avatar'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

defineProps({
  candidate: {
    type: Object,
    required: true,
  },
})
</script>
