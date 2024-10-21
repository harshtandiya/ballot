<template>
  <div class="p-4 flex flex-col gap-4">
    <div class="border-b mb-2 pb-4 space-y-2">
      <h3 class="text-sm uppercase font-medium text-primary-600">Manage</h3>
      <h1 class="text-3xl font-semibold font-sans">Candidates</h1>
      <p class="text-sm text-primary-600">
        Create candidate forms and manage submissions
      </p>
    </div>
    <div v-if="!has_form.data" class="space-y-3">
      <div class="space-y-2">
        <h4 class="text-base font-medium text-primary-800">
          Form has not been created
        </h4>
        <p class="text-sm text-primary-700">
          Create a nomination form to accept applications for election
          candidates.
        </p>
      </div>
      <Button
        label="Create Form"
        variant="solid"
        :route="`/create-nomination-form?election=${route.params.id}`"
      />
    </div>
    <div v-else>
      <div v-if="nominationForm.loading">
        <LoadingText />
      </div>
      <div v-if="nominationForm.data">
        <div class="space-y-2">
          <h4 class="text-lg font-medium text-primary-800">
            Form is
            <span
              class="font-semibold"
              :class="
                { Live: 'text-green-700', Closed: 'text-red-700' }[
                  nominationForm.data.status
                ]
              "
              >{{ nominationForm.data.status }}</span
            >
          </h4>
          <p class="text-sm text-primary-700">
            The candidate form has been created. You can add or modify fields of
            the form.
          </p>
          <Button
            label="Manage Form"
            variant="solid"
            :route="{
              name: 'Manage Candidate Form',
              params: { id: nominationForm.data.name },
            }"
          />
        </div>
        <InsightsView :nomination-form="nominationForm" class="my-6" />
      </div>
    </div>
  </div>
</template>
<script setup>
import { createResource, LoadingText } from 'frappe-ui'
import { useRoute } from 'vue-router'
import { toast } from 'vue-sonner'
import InsightsView from '@/components/nominations/Insights.vue'

const route = useRoute()

const has_form = createResource({
  url: 'ballot.api.election.has_nomination_form',
  makeParams() {
    return {
      election: route.params.id,
    }
  },
  auto: true,
  onSuccess(data) {
    if (!data) {
      return
    }
    nominationForm.fetch()
  },
})

const nominationForm = createResource({
  url: 'frappe.client.get',
  makeParams() {
    return {
      doctype: 'Election Nomination Form',
      filters: {
        election: route.params.id,
      },
    }
  },
  onError(err) {
    toast.error(err.messages)
  },
})
</script>
