<template>
  <div class="px-4 py-6 flex flex-col gap-6">
    <div>
      <h1 class="text-3xl font-sans font-bold tracking-wide mb-2">
        My Workspace
      </h1>
      <p class="text-base text-gray-600">
        Welcome to your dashboard. Here you can view all your elections and
        manage your account.
      </p>
    </div>
    <TeamSection />
  </div>
</template>
<script setup>
import TeamSection from '@/components/dashboard/TeamSection.vue'
</script>
