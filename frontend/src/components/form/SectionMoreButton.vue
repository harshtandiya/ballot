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

const emit = defineEmits([
  'add-section-below',
  'add-column',
  'remove-section',
  'remove-section-with-content',
])

const buttons = ref([
  {
    label: 'Add Section Below',
    onClick: () => {
      emit('add-section-below')
    },
  },
  {
    label: 'Add Column',
    onClick: () => {
      emit('add-column')
    },
  },
  {
    label: 'Remove Section',
    onClick: () => {
      emit('remove-section')
    },
  },
  {
    label: 'Remove Section + Fields',
    theme: 'red',
    onClick: () => {
      emit('remove-section-with-content')
    },
  },
])
</script>
