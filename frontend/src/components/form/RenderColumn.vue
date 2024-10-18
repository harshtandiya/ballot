<template>
  <div class="w-full">
    <RenderField
      v-model:fields="fields"
      :field="fields[getFieldIndex(fields, column)]"
    />
    <div class="flex flex-col gap-1">
      <RenderField
        v-for="_field in columnFields"
        :key="_field.fieldname"
        v-model:fields="fields"
        :field="_field"
      />
    </div>
  </div>
</template>
<script setup>
import RenderField from './RenderField.vue'
import { getFieldIndex } from '@/utils/formbuilder'

const fields = defineModel('fields', { type: Array, required: true })

const props = defineProps({
  columnFields: {
    type: Array,
    required: true,
  },
  column: {
    type: Array,
    required: true,
  },
})
</script>
