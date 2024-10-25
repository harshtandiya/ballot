<template>
  <div
    class="flex flex-col md:flex-row gap-4 justify-between items-center p-4 bg-primary-50 border rounded"
  >
    <div>
      <div v-if="hasForm">
        <div v-if="form.status == 'Live'" class="space-y-1">
          <div class="flex items-center gap-3">
            <LivePing />
            <h4 class="text-lg font-semibold text-primary-800">
              Candidate applications are live!
            </h4>
          </div>
          <p class="text-sm text-primary-500">
            Apply to become a candidate in this election.
          </p>
        </div>
        <div v-else>
          <h4 class="text-lg font-semibold text-primary-800">
            Candidate applications are closed.
          </h4>
        </div>
      </div>
      <div v-else>
        <h4 class="text-lg font-semibold text-primary-800">
          Candidate applications will open soon.
        </h4>
      </div>
    </div>
    <div class="w-full md:w-fit">
      <Button
        v-if="hasForm && form.status == 'Live'"
        class="w-full"
        variant="solid"
        label="Apply"
        icon-right="arrow-right"
        :route="{
          name: 'Nomination Form',
          params: { slug: route.params.slug },
        }"
      />
    </div>
  </div>
</template>
<script setup>
import LivePing from '@/components/animations/LivePing.vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const props = defineProps({
  hasForm: {
    type: Boolean,
    required: true,
  },
  form: {
    type: Object,
    default() {
      return {}
    },
  },
})
</script>
