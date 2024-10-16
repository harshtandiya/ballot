<template>
  <EditFieldDialog
    v-model:fields="fields"
    v-model:show-dialog="showEditDialog"
    :selected-field="currentField"
    @delete-field="
      () => {
        emit('delete-field', currentField)
      }
    "
  />
  <div @dblclick.prevent="showEditDialog = true">
    <div
      v-if="
        currentField.fieldtype === 'Section Break' ||
        currentField.fieldtype === 'Column Break'
      "
    >
      <InputText
        v-model="fields[getFieldIndex(currentField)].label"
        :placeholder="`${currentField.fieldtype.split(' ')[0]} label`"
        class="!text-sm italic !p-0 !font-medium !border-none !shadow-none focus:border-none"
        :class="
          currentField.fieldtype === 'Section Break'
            ? '!bg-primary-50'
            : '!bg-white'
        "
      ></InputText>
    </div>
    <div
      v-else
      class="p-2 rounded border w-full bg-white flex flex-col gap-1 hover:border-solid hover:cursor-pointer"
      :class="[
        isSelected
          ? 'border-solid rounded border-primary-700'
          : 'border-dashed border-primary-400',
        {
          Data: 'max-w-[360px]',
          Number: 'max-w-[360px]',
          Select: 'max-w-[360px]',
          Editor: 'h-[180px]',
        }[currentField.fieldtype],
      ]"
    >
      <div class="flex justify-between items-center">
        <div>
          <span
            v-if="fields[getFieldIndex(currentField)].mandatory"
            class="text-red-500 text-sm ml-1"
          >
            *
          </span>
          <InputText
            v-model="fields[getFieldIndex(currentField)].label"
            placeholder="Field Label"
            class="!text-sm !w-fit !border-none !bg-none !p-0 !rounded !shadow-none focus:border-none"
          />
        </div>
        <Button
          size="sm"
          variant="ghost"
          @click="emit('delete-field', currentField)"
        >
          <IconTrash size="1rem" class="text-inherit" />
        </Button>
      </div>
      <component
        :is="getComponent(currentField.fieldtype)"
        size="small"
        disabled
        readonly
      ></component>
    </div>
  </div>
</template>
<script setup>
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Select from 'primevue/select'
import Editor from 'primevue/editor'
import Textarea from 'primevue/textarea'
import { IconTrash } from '@tabler/icons-vue'
import EditFieldDialog from './EditFieldDialog.vue'
import { ref } from 'vue'

const showEditDialog = ref(false)

const props = defineProps({
  isSelected: {
    type: Boolean,
    default: false,
  },
  currentField: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['load-field', 'delete-field'])

const fields = defineModel('fields', {
  type: Object,
  required: true,
})

function getComponent(type) {
  switch (type) {
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
    default:
      return InputText
  }
}

function getFieldIndex(_field) {
  return fields.value.findIndex((field) => field.fieldname === _field.fieldname)
}

const selectField = () => {
  emit('load-field', props.currentField)
}
</script>
