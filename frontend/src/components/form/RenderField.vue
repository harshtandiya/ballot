<template>
  <div class="w-full my-2">
    <div
      v-if="
        field.fieldtype === 'Section Break' ||
        field.fieldtype === 'Column Break'
      "
    >
      <h3
        v-if="field.label"
        class="font-medium"
        :class="field.fieldtype === 'Section Break' ? 'text-xl' : 'text-lg'"
      >
        {{ field.label }}
      </h3>
      <div
        v-else
        :class="field.fieldtype == 'Section Break' ? 'hidden' : 'h-4'"
      ></div>
    </div>
    <div v-else class="flex flex-col gap-2 h-fit">
      <div class="flex items-start gap-1">
        <label :for="field.fieldname" class="text-sm">{{ field.label }}</label>
        <IconAsterisk v-if="field.mandatory" color="red" size="0.5rem" />
      </div>
      <component
        :is="getComponent"
        id="field.fieldname"
        v-model="fields[getFieldIndex(field.fieldname)]['value']"
        :options="field.options.split('\n')"
        class="h-full"
        :class="{ Editor: 'h-[200px]' }[field.fieldtype]"
      ></component>
    </div>
  </div>
</template>
<script setup>
import InputText from 'primevue/inputtext'
import Editor from 'primevue/editor'
import InputNumber from 'primevue/inputnumber'
import Select from 'primevue/select'
import Checkbox from 'primevue/checkbox'
import Textarea from 'primevue/textarea'
import FloatLabel from 'primevue/floatlabel'
import { computed } from 'vue'
import { IconAsterisk } from '@tabler/icons-vue'

const props = defineProps({
  field: {
    type: Object,
    required: true,
  },
})

const fields = defineModel('fields', {
  type: Object,
  required: true,
})

const getComponent = computed(() => {
  switch (props.field.fieldtype) {
    case 'Data':
      return InputText
    case 'Number':
      return InputNumber
    case 'Select':
      return Select
    case 'Editor':
      return Editor
    case 'Textarea':
      return Textarea
    case 'Checkbox':
      return Checkbox
    default:
      return InputText
  }
})

function getFieldIndex(fieldname) {
  return fields.value.findIndex((field) => field.fieldname === fieldname)
}
</script>
