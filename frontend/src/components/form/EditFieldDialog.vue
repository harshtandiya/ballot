<template>
  <Dialog
    v-model="showDialog"
    :options="{
      title: 'Edit Field',
      actions: [
        {
          label: 'Save',
          variant: 'solid',
          onClick: () => {
            showDialog = false
          },
        },
        {
          label: 'Delete',
          theme: 'red',
          onClick: () => {
            emit('delete-field')
          },
        },
      ],
    }"
  >
    <template #body-content>
      <div class="flex flex-col gap-2">
        <FormControl
          v-for="f in editableFields"
          :key="f.fieldname"
          v-model="
            fields[getIndexFromFieldname(selectedField.fieldname)][f.fieldname]
          "
          :type="f.type"
          :label="f.label"
        />
      </div>
    </template>
  </Dialog>
</template>
<script setup>
import { Dialog, FormControl } from 'frappe-ui'
import { ref } from 'vue'

const fields = defineModel('fields', { type: Array })
const showDialog = defineModel('showDialog', { type: Boolean, default: false })

const props = defineProps({
  selectedField: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['delete-field'])

const editableFields = ref([
  {
    label: 'Label',
    fieldname: 'label',
    type: 'text',
  },
  {
    label: 'Fieldname',
    fieldname: 'fieldname',
    type: 'text',
  },
  {
    label: 'Options',
    fieldname: 'options',
    type: 'textarea',
  },
  {
    label: 'Mandatory',
    fieldname: 'mandatory',
    type: 'checkbox',
  },
])

const getIndexFromFieldname = (fieldname) => {
  return props.fields.findIndex((field) => field.fieldname === fieldname)
}
</script>
