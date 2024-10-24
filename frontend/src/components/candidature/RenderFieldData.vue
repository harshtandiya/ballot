<template>
  <div v-if="field.fieldtype === 'Checkbox'" class="flex items-center gap-2">
    <Checkbox :id="field.fieldname" :value="field.value" disabled />
    <label :for="field.fieldname" class="text-base font-medium">
      {{ field.label }}
    </label>
  </div>
  <div v-else>
    <Fieldset :toggleable="true">
      <template #legend="{ toggleCallback }">
        <div
          class="flex gap-1"
          @click="
            () => {
              toggleCallback()
              toggleState = !toggleState
            }
          "
        >
          <IconChevronUp
            size="1rem"
            class="transition-all"
            :class="toggleState ? '' : ' -rotate-180'"
          />
          <label class="text-base font-medium">
            {{ field.label }}
          </label>
        </div>
      </template>
      <div
        v-if="field.fieldtype === 'Editor'"
        class="text-base"
        v-html="field.value"
      ></div>
      <p v-else class="text-base mt-2">{{ field.value || 'No response' }}</p>
    </Fieldset>
  </div>
</template>
<script setup>
import Fieldset from 'primevue/fieldset'
import Checkbox from 'primevue/checkbox'
import { IconChevronUp } from '@tabler/icons-vue'
import { ref } from 'vue'
const props = defineProps({
  field: {
    type: Object,
    required: true,
  },
})

const toggleState = ref(false)
</script>
