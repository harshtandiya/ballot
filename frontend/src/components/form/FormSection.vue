<template>
  <div
    class="w-full bg-primary-50 border min-h-16 rounded text-base p-3 space-y-2"
  >
    <div class="w-full flex justify-between items-center">
      <Field
        v-model:fields="fields"
        :current-field="{
          fieldtype: 'Section Break',
          fieldname: section,
          label: '',
        }"
        :is-selected="isSelected(selectedField, section)"
      />
      <SectionMoreButton
        @add-section-below="handleAddSectionBelow(section)"
        @add-column="handleAddColumn(section)"
        @remove-section="handleRemoveSection(section)"
        @remove-section-with-content="handleRemoveSectionWithData(section)"
      />
    </div>
    <div :class="`grid grid-cols-1 md:grid-cols-${values.column_count} gap-2`">
      <FormColumn
        v-for="(_fields, column) in values.columns"
        :key="column"
        v-model:fields="fields"
        :column="column"
        :column-fields="_fields"
        :section="section"
        :selected-field="selectedField"
        @load-field="(fieldToLoad) => emit('load-field', fieldToLoad)"
      />
    </div>
  </div>
</template>
<script setup>
import Field from './Field.vue'
import FormColumn from './FormColumn.vue'
import SectionMoreButton from './SectionMoreButton.vue'
import {
  addSectionBelow,
  addColumn,
  deleteSection,
  deleteSectionWithContent,
  isSelected,
} from '@/utils/formbuilder'

const fields = defineModel('fields', { type: Array, required: true })

const props = defineProps({
  values: {
    type: Object,
    required: true,
  },
  section: {
    type: String,
    required: true,
  },
  selectedField: {
    type: Object,
    required: false,
    default() {
      return {}
    },
  },
})

const emit = defineEmits(['load-field'])

function handleAddSectionBelow(section) {
  addSectionBelow(fields, section)
}

function handleAddColumn(section) {
  addColumn(fields, section)
}

function handleRemoveSection(section) {
  deleteSection(fields, section)
}

function handleRemoveSectionWithData(section) {
  deleteSectionWithContent(fields, section)
}
</script>
