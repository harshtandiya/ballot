<template>
  <Dialog
    v-model="showErrorDialog"
    :options="{
      title: 'Error',
    }"
  >
    <template #body-content>
      <ErrorMessage :message="errorMessages" />
    </template>
  </Dialog>
  <div class="flex">
    <Sidebar>
      <template #pre-nav-items>
        <Button
          label="Go Back"
          icon-left="arrow-left"
          variant="ghost"
          size="sm"
          class="!justify-start font-medium"
          @click="router.back()"
        ></Button>
      </template>
      <template #nav-items>
        <div class="flex flex-col gap-2">
          <h3 class="text-base font-medium border-b pb-2">
            Edit Candidate Form
          </h3>
          <p class="text-sm text-primary-600">
            Design and customize a form to collect applications from potential
            election candidates.
          </p>
        </div>
      </template>
    </Sidebar>
    <div v-if="candidateForm.data" class="w-full md:ml-[220px]">
      <div class="w-full flex justify-between items-center p-4">
        <h1 class="font-sans text-3xl font-semibold">Candidate Form</h1>
        <Button
          label="Update Form"
          variant="solid"
          size="lg"
          @click="handleFormSave"
        />
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 m-4">
        <div class="flex items-start col-span-2 gap-2 mb-3">
          <Checkbox
            id="accept_incoming_applications"
            v-model="candidateForm.data.accept_incoming_applications"
            binary
          />
          <div class="flex flex-col items-start">
            <label
              for="accept_incoming_applications"
              class="text-base font-medium"
            >
              Accept All Incoming Applications
            </label>
            <small class="text-primary-600">
              Accept all the incoming candidature applications automatically
            </small>
          </div>
        </div>
        <FloatLabel variant="on">
          <Select
            id="formStatus"
            v-model="candidateForm.data.status"
            :options="statusOptions"
            class="w-full"
          />
          <label for="formStatus">Status</label>
        </FloatLabel>
        <div class="space-y-1">
          <div class="text-base">
            The form will be available at the link below:
          </div>
          <Chip v-if="election.data">
            <a :href="formRoute" class="text-sm font-mono" target="_blank">
              {{ formRoute }}
            </a>
          </Chip>
        </div>
        <div class="col-span-2">
          <label for="description" class="text-sm text-primary-600"
            >Description</label
          >
          <Editor
            id="description"
            v-model="candidateForm.data.description"
            class="mb-6"
          />
        </div>
      </div>
      <div>
        <h3 class="text-lg ml-4 mb-4 text-primary-700 font-semibold">Fields</h3>
        <FormBaseFields />
        <FormBuilder v-model:fields="fields" />
      </div>
    </div>
  </div>
</template>
<script setup>
import FloatLabel from 'primevue/floatlabel'
import Select from 'primevue/select'
import Editor from 'primevue/editor'
import Chip from 'primevue/chip'
import Checkbox from 'primevue/checkbox'
import Sidebar from '@/components/Sidebar.vue'
import FormBaseFields from '@/components/candidature/FormBaseFields.vue'
import FormBuilder from '@/components/form/Builder.vue'
import { useRouter, useRoute } from 'vue-router'
import { createResource, Dialog, ErrorMessage } from 'frappe-ui'
import { computed, ref } from 'vue'
import { getFieldErrors } from '@/utils/formValidators'
import { toast } from 'vue-sonner'

const router = useRouter()
const route = useRoute()
const fields = ref([])
const showErrorDialog = ref(false)
const errorMessages = ref('')

const statusOptions = ref(['Live', 'Draft', 'Closed'])

const candidateForm = createResource({
  url: 'frappe.client.get',
  makeParams() {
    return {
      doctype: 'Election Nomination Form',
      name: route.params.id,
    }
  },
  auto: true,
  onSuccess(data) {
    election.fetch()
    fields.value = JSON.parse(data.fields_meta)
  },
})

const election = createResource({
  url: 'frappe.client.get',
  makeParams() {
    return {
      doctype: 'Election',
      name: candidateForm.data.election,
    }
  },
})

const handleFormSave = () => {
  errorMessages.value = ''

  const errors = []
  fields.value.forEach((field) => {
    const validationErrors = getFieldErrors(field)
    if (validationErrors.length) {
      errors.push(...validationErrors)
    }
  })

  if (errors.length) {
    errorMessages.value = errors.join('\n')
    showErrorDialog.value = true
    return
  }

  saveForm.fetch()
}

const saveForm = createResource({
  url: 'frappe.client.set_value',
  makeParams() {
    return {
      doctype: 'Election Nomination Form',
      name: route.params.id,
      fieldname: {
        accept_incoming_applications:
          candidateForm.data.accept_incoming_applications,
        status: candidateForm.data.status,
        description: candidateForm.data.description,
        fields_meta: JSON.stringify(fields.value),
      },
    }
  },
  onSuccess() {
    errorMessages.value = ''
    toast.success('Updated form successfully!')
  },
  onError(err) {
    errorMessages.value = err.messages
    showErrorDialog.value = true
  },
})

const formRoute = computed(() => {
  let route = `${window.location.origin}/ballot/election/${election.data?.slug}/apply`

  return route
})
</script>
