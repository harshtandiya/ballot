<template>
  <div class="w-full flex flex-col">
    <RenderBaseFields
      v-model:fields="baseFieldsData"
      :submission="submission"
    />
    <RenderSection
      v-for="(values, section) in transformedFields"
      :key="section"
      :fields="fieldsData"
      :values="values"
      :section="section"
      :submission="submission"
    />
    <ErrorMessage class="my-2" :message="errorMessages" />
    <Button
      class="w-full md:w-1/3"
      label="Save"
      variant="solid"
      @click="handleUpdate"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import RenderBaseFields from '@/components/candidature/RenderBaseFields.vue'
import RenderSection from '../form/RenderSection.vue'
import { transformFields } from '@/utils/formbuilder'
import { ErrorMessage } from 'frappe-ui'

const submission = defineModel({ required: true, type: Object })

const emit = defineEmits(['update-submission'])

const errorMessages = ref('')

// Initialize base fields with values from submission if they exist
const baseFieldsData = ref([
  {
    label: 'Photo',
    fieldname: 'photo',
    type: 'Attach Image',
    mandatory: false,
    value: submission.value?.photo || '',
  },
  {
    label: 'Full Name',
    fieldname: 'full_name',
    type: 'data',
    mandatory: true,
    value: submission.value?.full_name || '',
  },
  {
    label: 'Email',
    fieldname: 'email',
    type: 'data',
    mandatory: true,
    value: submission.value?.email || '',
  },
  {
    label: 'Designation',
    fieldname: 'designation',
    type: 'data',
    mandatory: true,
    value: submission.value?.designation || '',
  },
  {
    label: 'Organization',
    fieldname: 'organization',
    type: 'data',
    mandatory: true,
    value: submission.value?.organization || '',
  },
])

// Initialize fields data from submission meta if it exists
const fieldsData = ref(
  submission.value?.submission_meta
    ? JSON.parse(submission.value.submission_meta)
    : [],
)

// Transform fields for section rendering
const transformedFields = computed(() => {
  return transformFields(fieldsData.value)
})

// Watch for changes in baseFieldsData and update submission
watch(
  baseFieldsData,
  (newValues) => {
    submission.value = {
      ...submission.value,
      photo: newValues[0].value,
      full_name: newValues[1].value,
      email: newValues[2].value,
      designation: newValues[3].value,
      organization: newValues[4].value,
    }
  },
  { deep: true },
)

// Watch for changes in fieldsData and update submission
watch(
  fieldsData,
  (newValues) => {
    submission.value = {
      ...submission.value,
      submission_meta: JSON.stringify(newValues),
    }
  },
  { deep: true },
)

function getMandatoryErrors() {
  let errors = []

  // Check base fields using baseFieldsData
  baseFieldsData.value.forEach((field) => {
    if (field.mandatory && !field.value) {
      errors.push(`${field.label} is mandatory`)
    }
  })

  // Check section fields using fieldsData
  fieldsData.value.forEach((field) => {
    if (field.mandatory && !field.value) {
      errors.push(`${field.label} is mandatory`)
    }
  })

  return errors
}
const handleUpdate = () => {
  let errors = getMandatoryErrors()

  if (errors.length) {
    errorMessages.value = errors.join('\n')
    return
  }

  errorMessages.value = ''

  emit('update-submission')
}
</script>
