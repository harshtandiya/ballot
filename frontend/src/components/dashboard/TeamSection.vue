<template>
  <CreateTeamDialog v-model="showDialog" @reload-teams="teams.fetch()" />
  <div>
    <h3 class="text-lg uppercase font-medium font-sans">My Teams</h3>
    <div class="my-4">
      <Button
        class="w-fit text-base"
        size="sm"
        @click="() => (showDialog = true)"
        >Create Team</Button
      >
    </div>
    <div v-if="teams.loading">
      <span class="text-sm">Loading your teams...</span>
    </div>
    <div v-if="teams.data?.length == 0" class="flex flex-col gap-2">
      <span class="text-sm text-gray-700">You are not part of any team.</span>
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-3">
      <TeamCard v-for="(team, index) in teams.data" :key="index" :team="team" />
    </div>
  </div>
</template>
<script setup>
import { inject, ref } from 'vue'
import { createResource } from 'frappe-ui'
import CreateTeamDialog from '@/components/dashboard/CreateTeamDialog.vue'
import TeamCard from '@/components/dashboard/TeamCard.vue'

const session = inject('$session')
const showDialog = ref(false)

const teams = createResource({
  url: 'ballot.api.team.get_user_teams',
  makeParams() {
    return {
      user: session.user,
    }
  },
  auto: true,
})
</script>
