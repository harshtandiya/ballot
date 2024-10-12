<template>
  <div v-if="team.data" class="p-4 flex flex-col gap-4">
    <div class="border-b">
      <h3 class="text-sm uppercase font-medium text-primary-600">
        Team Details
      </h3>
      <h1 class="mt-2 mb-4 text-3xl font-semibold font-sans">
        {{ team.data.team_name }}
      </h1>
    </div>
    <div class="space-y-2">
      <div class="grid grid-cols-1 md:grid-cols-2 mt-3">
        <FloatLabel variant="on">
          <InputText
            id="team_name"
            v-model="team_name"
            label="Team Name"
            class="w-full"
          />
          <label for="team_name">Team Name</label>
        </FloatLabel>
      </div>
      <ErrorMessage :message="errorMessage" />
      <Button label="Update" variant="solid" @click="updateName.fetch()" />
    </div>
    <div>
      <div class="mt-4 mb-2 space-y-2">
        <h4 class="text-base font-medium">Members</h4>
        <AddMemberDialog @reload-members="members.fetch()" />
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 my-4">
        <MemberCard
          v-for="(member, index) in members.data"
          :key="index"
          :member="member"
        />
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { createResource, ErrorMessage } from 'frappe-ui'
import { useRoute } from 'vue-router'
import { toast } from 'vue-sonner'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import MemberCard from '@/components/team/MemberCard.vue'
import AddMemberDialog from '@/components/team/AddMemberDialog.vue'

const route = useRoute()
const team_name = ref('')
const errorMessage = ref('')

const team = createResource({
  url: 'frappe.client.get',
  makeParams() {
    return {
      doctype: 'Election Team',
      name: route.params.id,
    }
  },
  auto: true,
  onSuccess(data) {
    members.fetch()
    team_name.value = data.team_name
  },
})

const members = createResource({
  url: 'ballot.api.team.get_member_details',
  makeParams() {
    return {
      team: route.params.id,
    }
  },
  loading: true,
})

const updateName = createResource({
  url: 'frappe.client.set_value',
  makeParams() {
    return {
      doctype: 'Election Team',
      name: route.params.id,
      fieldname: 'team_name',
      value: team_name.value,
    }
  },
  onSuccess() {
    errorMessage.value = ''
    toast.success('Team name updated!')
    team.fetch()
  },
  onError(err) {
    errorMessage.value = err.messages
  },
})
</script>
