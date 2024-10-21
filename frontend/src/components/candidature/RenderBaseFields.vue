<template>
  <div class="flex flex-col gap-2 mb-4">
    <h3 class="text-lg text-primary-700 font-medium mb-2">Personal Details</h3>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
      <div
        v-for="(field, index) in fields"
        :key="field.fieldname"
        class="flex flex-col gap-2 h-fit"
      >
        <div class="flex items-start gap-1">
          <label :for="field.fieldname" class="text-sm">
            {{ field.label }}
          </label>
          <IconAsterisk v-if="field.mandatory" color="red" size="0.5rem" />
        </div>
        <InputText :id="field.fieldname" v-model="fields[index]['value']" />
      </div>
    </div>
  </div>
</template>
<script setup>
import InputText from 'primevue/inputtext'
import { IconAsterisk } from '@tabler/icons-vue'

const fields = defineModel('fields', {
  type: Array,
  required: true,
})
</script>
