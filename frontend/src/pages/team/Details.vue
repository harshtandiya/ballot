<template>
  <div class="p-4">
    <h3 class="text-sm uppercase font-sans font-medium text-primary-600">
      Team Details
    </h3>
    <h1 class="mt-2 mb-4 text-3xl font-semibold font-sans">
      {{ team.team_name }}
    </h1>
  </div>
</template>
<script setup>
import { inject } from 'vue'

const team = inject('$team')
</script>
