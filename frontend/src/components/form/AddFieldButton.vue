<template>
  <Button variant="subtle" label="Add field" @click="toggle" />
  <Popover ref="op">
    <div class="flex flex-col">
      <Button
        v-for="(b, index) in buttons"
        :key="index"
        :label="b"
        variant="ghost"
        size="sm"
        class="!text-sm !justify-start"
        @click="emit('add-field', b)"
      />
    </div>
  </Popover>
</template>
<script setup>
import { ref } from 'vue'
import { getFieldTypes } from '@/utils/formbuilder'
import Popover from 'primevue/popover'

const op = ref()
const toggle = (event) => {
  op.value.toggle(event)
}

const emit = defineEmits(['add-field'])

const buttons = getFieldTypes().filter((val) => {
  return val != 'Section Break' && val != 'Column Break'
})
</script>
