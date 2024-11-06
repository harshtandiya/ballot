<template>
  <div
    class="opacity-90 bg-primary-50 border min-h-16 rounded text-base p-3 space-y-2 mx-4 cursor-not-allowed"
  >
    <div class="text-sm italic font-medium text-primary-400">
      Personal Details
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
      <div
        v-for="field in baseFields"
        :key="field.label"
        class="w-full cursor-not-allowed bg-white border min-h-16 rounded text-base p-3 space-y-2"
      >
        <div class="flex justify-between items-center">
          <div class="space-y-1">
            <div class="flex gap-2">
              <label
                class="text-sm cursor-not-allowed text-primary-500"
                :for="field.id"
                >{{ field.label }}</label
              >
              <span v-if="field.mandatory" class="text-red-500 text-sm ml-1">
                *
              </span>
            </div>
            <div v-if="field.type == 'Attach Image'" class="cursor-not-allowed">
              <Button label="Upload Image" disabled />
            </div>
            <InputText
              v-else
              :id="field.id"
              class="cursor-not-allowed"
              disabled
            />
          </div>
        </div>
      </div>
    </div>
    <div class="text-primary-600 text-sm mt-2">
      These fields are required and cannot be removed.
    </div>
  </div>
</template>
<script setup>
import InputText from 'primevue/inputtext'
import { ref } from 'vue'

const baseFields = ref([
  {
    label: 'Photo',
    id: 'photo',
    mandatory: false,
    type: 'Attach Image',
  },
  {
    label: 'Full Name',
    id: 'full_name',
    mandatory: true,
    type: 'Data',
  },
  {
    label: 'Email',
    id: 'email',
    mandatory: true,
    type: 'Data',
  },
  {
    label: 'Designation',
    id: 'designation',
    mandatory: true,
    type: 'Data',
  },
  {
    label: 'Organization',
    id: 'organization',
    mandatory: true,
    type: 'Data',
  },
])
</script>
