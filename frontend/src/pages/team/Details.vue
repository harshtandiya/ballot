<template>
  <div v-if="team.loading"><LoadingText /></div>
  <div v-else class="p-4 flex flex-col gap-4">
    <div class="border-b">
      <h3 class="text-sm uppercase font-medium text-primary-600">
        Team Details
      </h3>
      <h1 class="mt-2 mb-4 text-3xl font-semibold font-sans">
        {{ team.doc?.team_name }}
      </h1>
    </div>
    <div class="space-y-2">
      <div class="grid grid-cols-1 md:grid-cols-2 mt-3">
        <FloatLabel variant="on">
          <InputText
            id="team_name"
            v-model="teamName"
            label="Team Name"
            class="w-full"
          />
          <label for="team_name">Team Name</label>
        </FloatLabel>
      </div>
      <ErrorMessage :message="errorMessage" />
      <Button label="Update" variant="solid" @click="updateName" />
    </div>
    <div>
      <div class="mt-4 mb-2 space-y-2">
        <h4 class="text-base font-medium">Members</h4>
        <AddMemberDialog @reload-members="members.fetch()" />
      </div>
      <div
        v-if="members.data"
        class="grid grid-cols-1 md:grid-cols-3 gap-4 my-4"
      >
        <MemberCard
          v-for="(member, index) in members.data"
          :key="index"
          :member="member"
        />
      </div>
      <LoadingText v-else />
    </div>
  </div>
</template>
<script setup>
import { inject, ref, watch } from 'vue'
import { createResource, ErrorMessage, LoadingText } from 'frappe-ui'
import { useRoute } from 'vue-router'
import { toast } from 'vue-sonner'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import MemberCard from '@/components/team/MemberCard.vue'
import AddMemberDialog from '@/components/team/AddMemberDialog.vue'

const route = useRoute()
const errorMessage = ref('')

const team = inject('$team')

const teamName = ref(team.doc ? team.doc.team_name : '')

watch(
  () => team.doc,
  (newDoc) => {
    if (newDoc != null) {
      teamName.value = newDoc.team_name
    }
  },
)

const members = createResource({
  url: 'ballot.api.team.get_member_details',
  makeParams() {
    return {
      team: route.params.id,
    }
  },
  auto: true,
})

const updateName = () => {
  if (!teamName.value) {
    errorMessage.value = 'Team name cannot be null'
    return
  }

  errorMessage.value = ''
  team.setValue
    .submit({
      team_name: teamName.value,
    })
    .then(() => {
      toast.success('Team Details Updated')
    })
}
</script>
