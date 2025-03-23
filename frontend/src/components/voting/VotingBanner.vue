<template>
  <div
    class="flex flex-col md:flex-row gap-4 justify-between items-center p-4 bg-primary-50 border rounded"
  >
    <div class="flex flex-col items-center md:items-start gap-1">
      <div class="flex items-center gap-3">
        <LivePing v-if="status == 'Live'" />
        <h4 class="text-lg font-semibold text-primary-800">
          Voting is {{ status }}
        </h4>
      </div>
      <p class="text-sm text-primary-500">
        {{
          status == 'Live'
            ? 'Vote for your favourite candidate!'
            : 'Voting is closed'
        }}
      </p>
    </div>
    <Button
      label="Vote Now"
      variant="solid"
      class="w-full md:w-fit"
      @click="
        $router.push({
          name: 'Vote Form',
          params: { slug: $route.params.slug },
        })
      "
    />
  </div>
</template>
<script setup>
import LivePing from '@/components/animations/LivePing.vue'

defineProps({
  status: {
    type: String,
    required: true,
  },
})
</script>
