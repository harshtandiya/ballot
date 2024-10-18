<template>
  <div class="w-full flex flex-col">
    <RenderSection
      v-for="(values, section) in transformedFields"
      :key="section"
      v-model:fields="fields"
      :values="values"
      :section="section"
    />
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
import RenderField from './RenderField.vue'
import { createResource, ErrorMessage } from 'frappe-ui'
import { useRouter } from 'vue-router'
import RenderSection from './RenderSection.vue'

const fields = defineModel('fields', { type: Array, required: true })

const router = useRouter()

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
