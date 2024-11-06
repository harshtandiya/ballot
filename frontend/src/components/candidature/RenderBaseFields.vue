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
        <div v-if="field.type == 'Attach Image'" class="flex gap-2">
          <img
            v-if="field.value"
            :src="field.value"
            class="w-16 h-16 rounded-sm"
          />
          <div
            v-else
            class="w-16 h-16 rounded-sm bg-gray-100 items-center justify-center flex"
          >
            <IconUser size="1.5rem" />
          </div>
          <FileUploader
            :file-types="'image/*'"
            :validate-file="validateFile"
            @success="
              (file) => {
                field.value = file.file_url
              }
            "
          >
            <template #default="{ progress, uploading, openFileSelector }">
              <Button
                :variant="'subtle'"
                size="sm"
                :label="
                  uploading
                    ? `Uploading ${progress}`
                    : field.value
                      ? 'Re-Upload'
                      : 'Upload Image'
                "
                @click="openFileSelector"
              />
            </template>
          </FileUploader>
          <Button
            v-if="field.value"
            label="Remove"
            theme="red"
            @click="
              () => {
                field.value = ''
              }
            "
          />
        </div>
        <InputText
          v-else
          :id="field.fieldname"
          v-model="fields[index]['value']"
        />
      </div>
    </div>
  </div>
</template>
<script setup>
import InputText from 'primevue/inputtext'
import Avatar from 'primevue/avatar'
import { FileUploader } from 'frappe-ui'
import { IconAsterisk, IconUser } from '@tabler/icons-vue'

const fields = defineModel('fields', {
  type: Array,
  required: true,
})
</script>
