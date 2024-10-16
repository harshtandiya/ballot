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
            Create Nomination Form
          </h3>
          <div class="text-sm text-primary-600">
            <span> Election: {{ election.data?.title }} </span>
          </div>
          <p class="text-sm text-primary-600">
            Design and customize a form to collect applications from potential
            election candidates.
          </p>
        </div>
      </template>
    </Sidebar>
    <div class="w-full md:ml-[220px]">
      <div class="w-full flex justify-between items-center p-4">
        <h1 class="font-sans text-3xl font-semibold">Nomination Form</h1>
        <Button
          label="Create Form"
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

const election = createResource({
  url: 'frappe.client.get',
  makeParams() {
    return {
      doctype: 'Election',
      name: route.query.election,
    }
  },
  auto: true,
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

  createForm.fetch()
}

const createForm = createResource({
  url: 'frappe.client.insert',
  makeParams() {
    return {
      doc: {
        doctype: 'Election Nomination Form',
        election: route.query.election,
        fields_meta: JSON.stringify(fields.value),
      },
    }
  },
  onSuccess() {
    errorMessages.value = ''
    showErrorDialog.value = false

    toast.success('Form Created Successfully')
    router.replace({
      name: 'Nomination Dashboard',
      params: { id: route.query.election },
    })
  },
  onError(err) {
    errorMessages.value = err.messages + '\n\n' + err.message
    showErrorDialog.value = true
  },
})
</script>
