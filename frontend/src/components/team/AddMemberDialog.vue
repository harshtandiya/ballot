<template>
  <Button label="Add Member" class="w-fit" @click="showDialog = true" />
  <Dialog
    v-model="showDialog"
    :options="{
      title: 'Add Member',
      actions: [
        {
          label: 'Add',
          variant: 'solid',
          onClick: () => {
            addMember.fetch()
          },
        },
      ],
    }"
  >
    <template #body-content>
      <div class="flex flex-col gap-2">
        <span class="text-primary-700">Add member to your team.</span>
        <FloatLabel variant="on" class="mt-2">
          <InputText
            id="email"
            v-model="memberEmail"
            class="w-full"
            :invalid="isInvalid"
          />
          <label for="email">Email</label>
        </FloatLabel>
        <small class="text-primary-600">
          Please ensure the user you are adding is registered on the website.
        </small>
        <ErrorMessage :message="errorMessage" />
      </div>
    </template>
  </Dialog>
</template>
<script setup>
import { ref, watch } from 'vue'
import { Dialog, createResource, ErrorMessage } from 'frappe-ui'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import { useRoute } from 'vue-router'
import { toast } from 'vue-sonner'

const showDialog = ref(false)
const isInvalid = ref(false)
const memberEmail = ref('')
const errorMessage = ref('')

const route = useRoute()

const emit = defineEmits(['reload-members'])

const addMember = createResource({
  url: 'ballot.api.team.add_member_to_team',
  makeParams() {
    return {
      team: route.params.id,
      user: memberEmail.value,
    }
  },
  onSuccess() {
    toast.success('Member added successfully!')
    errorMessage.value = ''
    isInvalid.value = false
    emit('reload-members')
    showDialog.value = false
  },
  onError(err) {
    isInvalid.value = true
    errorMessage.value = err.messages
  },
})

watch(showDialog, () => {
  isInvalid.value = false
  errorMessage.value = ''
  memberEmail.value = ''
})
</script>
