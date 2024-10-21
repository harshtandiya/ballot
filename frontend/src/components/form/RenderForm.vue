<template>
  <div class="w-full flex flex-col">
    <RenderBaseFields v-model:fields="baseFields" />
    <RenderSection
      v-for="(values, section) in transformedFields"
      :key="section"
      v-model:fields="fields"
      :values="values"
      :section="section"
    />
    <ErrorMessage :message="errorMessages" />
    <Button
      label="Submit"
      variant="solid"
      class="w-full mt-4 md:w-1/3"
      @click="handleSubmit"
    />
  </div>
</template>
<script setup>
import { transformFields } from '@/utils/formbuilder'
import { computed, ref, inject } from 'vue'
import RenderBaseFields from '@/components/candidature/RenderBaseFields.vue'
import RenderField from './RenderField.vue'
import { createResource, ErrorMessage } from 'frappe-ui'
import { useRouter } from 'vue-router'
import RenderSection from './RenderSection.vue'

const fields = defineModel('fields', { type: Array, required: true })

const router = useRouter()

const baseFields = ref([
  {
    label: 'Full Name',
    fieldname: 'full_name',
    mandatory: true,
    value: '',
  },
  {
    label: 'Email',
    fieldname: 'email',
    mandatory: true,
    value: '',
  },
])

const props = defineProps({
  election: {
    type: Object,
    required: true,
  },
  form: {
    type: Object,
    required: true,
  },
})

const errorMessages = ref('')
const session = inject('$session')

const transformedFields = computed(() => {
  let _fields = transformFields(fields.value)
  return _fields
})

function getMandatoryErrors() {
  let errors = []

  baseFields.value.forEach((field) => {
    if (field.mandatory && !field.value) {
      errors.push(`${field.label} is mandatory`)
    }
  })

  fields.value.forEach((field) => {
    if (field.mandatory && !field.value) {
      errors.push(`${field.label} is mandatory`)
    }
  })

  return errors
}

const handleSubmit = () => {
  let errors = getMandatoryErrors()

  if (errors.length) {
    errorMessages.value = errors.join('\n')
    return
  }

  submitForm.fetch()
}

const submitForm = createResource({
  url: 'frappe.client.insert',
  makeParams() {
    return {
      doc: {
        doctype: 'Election Candidate Application',
        user: session.user,
        election: props.election.name,
        nomination_form: props.form.name,
        full_name: baseFields.value[0]['value'],
        email: baseFields.value[1]['value'],
        submission_meta: JSON.stringify(fields.value),
      },
    }
  },
  onSuccess() {
    errorMessages.value = ''
    router.replace({ name: 'My Submissions' })
  },
  onError(err) {
    errorMessages.value = err.errorMessages
  },
})
</script>
