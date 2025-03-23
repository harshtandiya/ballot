<template>
  <Button v-tooltip.bottom="tooltipText" icon="copy" @click="handleCopy()" />
</template>
<script setup>
import { ref } from 'vue'
import { copyToClipboard } from '@/utils/helpers.js'

const tooltipText = ref('Copy to clipboard')

const props = defineProps({
  valueToCopy: {
    type: String,
    required: true,
  },
})

const handleCopy = () => {
  tooltipText.value = 'Copied'
  copyToClipboard(props.value.valueToCopy)
  setTimeout(() => {
    tooltipText.value = 'Copy to clipboard'
  }, 1000)
}
</script>
