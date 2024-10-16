<template>
  <div class="form-layout-builder w-full flex flex-col gap-4">
    <Button
      v-if="!fields.length"
      label="Add Section"
      class="w-fit"
      @click="fields.push(getStandardFields('Section Break'))"
    />
    <FormSection
      v-for="(values, section) in transformedFields"
      :key="section"
      v-model:fields="fields"
      :values="values"
      :section="section"
      :selected-field="selectedField"
      @load-field="handleLoadField"
    />
  </div>
</template>

<script setup>
import FormSection from './FormSection.vue'
import { getStandardFields } from '@/utils/formbuilder'
import { computed, ref } from 'vue'

const fields = defineModel('fields', { type: Array, required: true })
const emit = defineEmits(['load-field'])

const selectedField = ref({})

const handleLoadField = (field) => {
  selectedField.value = field
  emit('load-field', field)
}

const transformedFields = computed(() => {
  const groupBySection = {}
  let curr_section = ''
  let curr_column = ''

  fields.value.forEach((field) => {
    switch (field.fieldtype) {
      case 'Section Break':
        curr_section = field.fieldname
        if (!groupBySection[curr_section]) {
          groupBySection[curr_section] = { column_count: 0, columns: {} }
        }
        curr_column = '' // Reset current column when a new section starts
        break

      case 'Column Break':
        curr_column = field.fieldname
        if (!groupBySection[curr_section].columns[curr_column]) {
          groupBySection[curr_section].column_count += 1
          groupBySection[curr_section].columns[curr_column] = []
        }
        break

      default:
        if (!groupBySection[curr_section]) {
          groupBySection[curr_section] = { column_count: 0, columns: {} }
        }
        if (!groupBySection[curr_section].columns[curr_column]) {
          groupBySection[curr_section].column_count += 1
          groupBySection[curr_section].columns[curr_column] = []
        }
        groupBySection[curr_section].columns[curr_column].push(field)
        break
    }
  })

  return groupBySection
})
</script>
