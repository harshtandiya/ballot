<template>
  <Button variant="ghost" icon="more-vertical" @click="toggle" />
  <Popover ref="op">
    <div class="flex flex-col">
      <Button
        v-for="(b, index) in buttons"
        :key="index"
        :label="b.label"
        variant="ghost"
        :theme="b.theme || 'gray'"
        size="sm"
        class="!text-sm !justify-start"
        @click="b.onClick"
      />
    </div>
  </Popover>
</template>
<script setup>
import Popover from 'primevue/popover'
import { ref } from 'vue'

const op = ref()
const toggle = (event) => {
  op.value.toggle(event)
}

const emit = defineEmits(['remove-column', 'remove-column-with-content'])

const buttons = ref([
  {
    label: 'Remove Column',
    onClick: () => {
      emit('remove-column')
    },
  },
  {
    label: 'Remove Column + Fields',
    theme: 'red',
    onClick: () => {
      emit('remove-column-with-content')
    },
  },
])
</script>
