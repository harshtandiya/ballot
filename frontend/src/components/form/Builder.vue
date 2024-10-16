<template>
  <div class="flex min-h-screen h-fit">
    <div class="flex-grow flex flex-col gap-4 p-4 mr-[220px]">
      <FormLayoutBuilder
        v-model:fields="fields"
        @load-field="
          ($event) => {
            selectedField = $event
          }
        "
      />
    </div>
    <!-- <AddFieldSidebar v-model:fields="fields" :selected-field="selectedField" /> -->
  </div>
</template>

<script setup>
import { onMounted, ref, onBeforeUnmount } from 'vue'
import AddFieldSidebar from './AddFieldSidebar.vue'
import FormLayoutBuilder from './FormLayoutBuilder.vue'
import { getStarterTemplate } from '@/utils/formbuilder'

const selectedField = ref({})

const fields = defineModel('fields', {
  type: Array,
  required: true,
})

onMounted(() => {
  if (!fields.value.length) {
    fields.value = getStarterTemplate()
  }
})
</script>
