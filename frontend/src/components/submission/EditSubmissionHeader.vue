<template>
  <div class="flex flex-col gap-3">
    <h1 class="text-3xl font-sans font-bold tracking-wide">Edit Submission</h1>
    <div
      v-if="election"
      class="flex gap-2 text-base text-primary-500 font-medium items-center"
    >
      <span>{{ election?.title }}</span>
      <IconCircleFilled class="w-2 h-2" />
      <Badge :label="`Form ${formStatus}`" :theme="getTheme" />
    </div>
    <hr />
  </div>
</template>
<script setup>
import { IconCircleFilled } from '@tabler/icons-vue'
import { Badge } from 'frappe-ui'
import { computed } from 'vue'
const props = defineProps({
  election: {
    type: Object,
    required: true,
  },
  formStatus: {
    type: String,
    default: '',
  },
})

const getTheme = computed(() => {
  if (!props.formStatus) {
    return
  }

  if (props.formStatus == 'Live') {
    return 'green'
  }

  return 'gray'
})
</script>
