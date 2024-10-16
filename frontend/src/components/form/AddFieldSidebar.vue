<template>
  <div
    class="w-[220px] min-h-screen fixed right-0 border-l bg-white p-4 flex flex-col gap-4"
  >
    <h2 class="text-xl font-medium">Manage Field</h2>
    <hr />
    <div v-if="!selectedField.fieldname" class="my-4 font-medium">
      <p class="text-base text-primary-600">
        Select a field to edit its properties.
      </p>
    </div>
    <div v-else class="space-y-4">
      <div v-for="f in sidebarFields" :key="f.fieldname">
        <FormControl
          v-model="
            fields[getIndexFromFieldname(selectedField.fieldname)][f.fieldname]
          "
          :label="f.label"
          :type="f.type"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Checkbox from 'primevue/checkbox'
import { FormControl } from 'frappe-ui'

const sidebarFields = ref([
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

const fields = defineModel('fields', {
  required: true,
  type: Array,
})

const props = defineProps({
  selectedField: {
    type: Object,
    required: false,
    default() {
      return {}
    },
  },
})

// Function to find the index of the field
const getIndexFromFieldname = (fieldname) => {
  return props.fields.findIndex((field) => field.fieldname === fieldname)
}
</script>
