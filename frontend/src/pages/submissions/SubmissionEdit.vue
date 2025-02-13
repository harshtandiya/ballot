<template>
  <div class="flex flex-col md:flex-row">
    <Sidebar>
      <template #pre-nav-items>
        <div>
          <Button
            label="Go Home"
            icon-left="arrow-left"
            variant="ghost"
            :route="`/`"
          />
        </div>
        <div class="space-y-2">
          <h4 class="text-sm uppercase mb-0 font-semibold">Edit Submission</h4>
          <p class="text-sm text-primary-500">
            Edit candidature submission. Changes can be made till the form is
            live.
          </p>
        </div>
      </template>
    </Sidebar>
    <div v-if="inLoading" class="w-full md:ml-[220px] px-4 py-6">
      <LoadingText />
    </div>
    <div
      v-if="!inLoading && formStatus.data"
      class="w-full md:ml-[220px] px-4 py-6 flex flex-col gap-6"
    >
      <EditSubmissionHeader
        :election="election.data"
        :form-status="formStatus.data.status"
      />
      <EditSubmissionForm
        v-model="submission.doc"
        @update-submission="updateSubmission"
      />
    </div>
  </div>
</template>
<script setup>
import Sidebar from '@/components/Sidebar.vue'
import { createDocumentResource, createResource, LoadingText } from 'frappe-ui'
import { useRoute } from 'vue-router'
import EditSubmissionHeader from '@/components/submission/EditSubmissionHeader.vue'
import EditSubmissionForm from '@/components/submission/EditSubmissionForm.vue'
import { ref, watch } from 'vue'
import { toast } from 'vue-sonner'

const route = useRoute()
const inLoading = ref(true)

const election = createResource({
  url: 'frappe.client.get_value',
  makeParams() {
    return {
      doctype: 'Election',
      fieldname: ['title', 'slug', 'name'],
      filters: {
        name: submission.doc.election,
      },
    }
  },
  auto: false,
  onSuccess(data) {
    if (data) {
      inLoading.value = false
    }
  },
  onError(err) {
    toast.error('Error fetching the election doc' + err.message)
  },
})

const formStatus = createResource({
  url: 'frappe.client.get_value',
  makeParams() {
    return {
      doctype: 'Election Nomination Form',
      filters: {
        election: submission.election,
      },
      fieldname: 'status',
    }
  },
})

const submission = createDocumentResource({
  doctype: 'Election Candidate Application',
  name: route.params.id,
  onError(err) {
    toast.error('Error fetching the submission' + err.message)
  },
})

watch(
  () => submission.doc,
  (newDoc) => {
    if (newDoc != null) {
      formStatus.fetch()
      election.fetch()
    }
  },
)

const updateSubmission = () => {
  submission.save.fetch().then(() => {
    toast.success('Saved')
  })
}
</script>
