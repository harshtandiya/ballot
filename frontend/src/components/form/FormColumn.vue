<template>
  <div
    class="w-full bg-white border min-h-16 rounded text-base p-3 space-y-2 hover:cursor-pointer hover:border-solid"
  >
    <div class="flex w-full justify-between align-center">
      <Field
        v-model:fields="fields"
        :current-field="{
          fieldtype: 'Column Break',
          fieldname: column,
          label: '',
        }"
        :is-selected="isSelected(selectedField, column)"
      />
      <ColumnMoreButton
        @remove-column="handleRemoveColumn"
        @remove-column-with-content="handleRemoveColumnWithContent"
      />
    </div>
    <div v-for="(f, index) in columnFields" :key="index" class="space-y-2">
      <Field
        v-model:fields="fields"
        :current-field="f"
        :is-selected="isSelected(selectedField, f.fieldname)"
        @load-field="
          (currentField) => {
            emit('load-field', currentField)
          }
        "
        @delete-field="(currentField) => handleDeleteField(currentField)"
      />
    </div>
    <AddFieldButton
      @add-field="(type) => handleAddField(section, column, type)"
    />
  </div>
</template>
<script setup>
import ColumnMoreButton from './ColumnMoreButton.vue'
import AddFieldButton from './AddFieldButton.vue'
import Field from './Field.vue'
import { addField } from '@/utils/formbuilder'
import {
  deleteColumn,
  deleteColumnWithContent,
  deleteField,
  isSelected,
} from '@/utils/formbuilder'

const emit = defineEmits(['load-field'])

const props = defineProps({
  columnFields: {
    type: Array,
    required: true,
  },
  column: {
    type: String,
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

const fields = defineModel('fields', { required: true, type: Array })

function handleAddField(section, column, type) {
  addField(fields, section, column, type)
}

function handleRemoveColumn() {
  deleteColumn(fields, props.section, props.column)
}

function handleRemoveColumnWithContent() {
  deleteColumnWithContent(fields, props.section, props.column)
}

function handleDeleteField(currentField) {
  deleteField(fields, currentField.fieldname)
}
</script>
