<template>
  <Card class="!shadow-none border border-primary-200">
    <template #header>
      <div class="ml-4 mt-4 font-medium font-sans">
        <Avatar
          v-if="member.user_image"
          :image="member.user_image"
          shape="circle"
        />
        <Avatar v-else :label="member.full_name.charAt(0)" shape="circle" />
      </div>
    </template>
    <template #content>{{ member.full_name }}</template>
  </Card>
</template>
<script setup>
import Avatar from 'primevue/avatar'
import Card from 'primevue/card'

defineProps({
  member: {
    type: Object,
    required: true,
  },
})
</script>
