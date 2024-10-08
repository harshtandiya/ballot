<template>
  <Dialog
    v-model="showDialog"
    class="z-50"
    :options="{
      title: 'Create Team',
      actions: [
        {
          label: 'Create',
          loading: createTeam.loading,
          variant: 'solid',
          size: 'md',
          onClick: () => {
            handleTeamCreate()
          },
        },
      ],
    }"
  >
    <template #body-content>
      <FloatLabel variant="on">
        <InputText
          id="team_name"
          v-model="team_name"
          class="w-full"
          :invalid="isInvalid"
        />
        <label for="team_name">Team Name</label>
      </FloatLabel>
      <ErrorMessage class="mt-2" :message="errorMessages" />
    </template>
  </Dialog>
</template>
<script setup>
import { Dialog, ErrorMessage } from 'frappe-ui'
import { ref } from 'vue'
import { createResource } from 'frappe-ui'
import { toast } from 'vue-sonner'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'

const team_name = ref('')
const isInvalid = ref(false)
const errorMessages = ref()

const showDialog = defineModel({
  type: Boolean,
  required: true,
})

const emit = defineEmits(['reload-teams'])

const handleTeamCreate = () => {
  if (!team_name.value) {
    errorMessages.value = 'Team name is required'
    isInvalid.value = true
    return
  }

  errorMessages.value = ''
  isInvalid.value = false

  createTeam.fetch()
}

const createTeam = createResource({
  url: 'ballot.api.team.create_team',
  makeParams() {
    return {
      team_name: team_name.value,
    }
  },
  onSuccess() {
    toast.success('Team Created Successfully!')
    team_name.value = ''
    showDialog.value = false
    emit('reload-teams')
  },
  onError(err) {
    toast.error('Error in creating teams!')
    errorMessages.value = err.messages
  },
})
</script>
