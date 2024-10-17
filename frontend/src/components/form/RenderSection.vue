<template>
  <div class="flex flex-col gap-3">
    <RenderField
      v-model:fields="fields"
      :field="fields[getFieldIndex(fields, section)]"
    />
    <div
      :class="`w-full grid grid-cols-1 md:grid-cols-${values.column_count} gap-4`"
    >
      <RenderColumn
        v-for="(_fields, column) in values.columns"
        :key="column"
        v-model:fields="fields"
        :column-fields="_fields"
        :column="column"
      />
    </div>
  </div>
</template>
<script setup>
import RenderColumn from './RenderColumn.vue'
import RenderField from './RenderField.vue'
import { getFieldIndex } from '@/utils/formbuilder'

const props = defineProps({
  values: {
    type: Object,
    required: true,
  },
  section: {
    type: String,
    required: true,
  },
})

const fields = defineModel('fields', { type: Array, required: true })
</script>
