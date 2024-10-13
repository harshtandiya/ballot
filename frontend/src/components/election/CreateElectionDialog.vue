<template>
  <Dialog
    v-model="showDialog"
    :options="{
      title: 'Draft New Election',
      actions: [
        {
          label: 'Create Draft',
          variant: 'solid',
          onClick: () => {
            createElection.fetch()
          },
        },
      ],
    }"
  >
    <template #body-content>
      <FloatLabel variant="on">
        <InputText
          id="election_name"
          v-model="electionName"
          :invalid="isInvalid"
          class="w-full"
        ></InputText>
        <label for="election_name">Election Title</label>
      </FloatLabel>
      <ErrorMessage :message="errorMessages" class="mt-2" />
    </template>
  </Dialog>
  <Button label="Create Election" variant="solid" @click="showDialog = true" />
</template>
<script setup>
import { Dialog, ErrorMessage, createResource } from 'frappe-ui'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import { ref } from 'vue'
import { toast } from 'vue-sonner'
import { useRoute } from 'vue-router'

const isInvalid = ref(false)
const electionName = ref('')
const showDialog = ref(false)
const errorMessages = ref('')
const route = useRoute()

const emit = defineEmits(['reload-elections'])

const createElection = createResource({
  url: 'frappe.client.insert',
  makeParams() {
    return {
      doc: {
        doctype: 'Election',
        title: electionName.value,
        organizing_team: route.params.id,
      },
    }
  },
  onSuccess() {
    isInvalid.value = false
    errorMessages.value = ''
    toast.info('Draft Election Created')
    emit('reload-elections')
    showDialog.value = false
  },
  onError(err) {
    isInvalid.value = true
    errorMessages.value = err.messages
  },
})
</script>
