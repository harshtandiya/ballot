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
    <div class="w-full md:ml-[220px]">
      <div class="w-full flex justify-between items-center p-4">
        <h1 class="font-sans text-3xl font-semibold">Candidate Form</h1>
        <Button
          label="Update Form"
          variant="solid"
          size="lg"
          @click="handleFormSave"
        />
      </div>
      <FormBuilder v-model:fields="fields" />
    </div>
  </div>
</template>
<script setup>
import Sidebar from '@/components/Sidebar.vue'
import FormBuilder from '@/components/form/Builder.vue'
import { useRouter, useRoute } from 'vue-router'
import { createResource, Dialog, ErrorMessage } from 'frappe-ui'
import { ref } from 'vue'
import { getFieldErrors } from '@/utils/formValidators'
import { toast } from 'vue-sonner'

const router = useRouter()
const route = useRoute()
const fields = ref([])
const showErrorDialog = ref(false)
const errorMessages = ref('')

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
    fields.value = JSON.parse(data.fields_meta)
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
      fieldname: 'fields_meta',
      value: JSON.stringify(fields.value),
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
</script>
