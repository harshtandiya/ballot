<template>
  <div>
    <router-view />
  </div>
</template>
<script setup>
import { session } from '@/data/session'
import { provide } from 'vue'

provide('$session', session)
</script>
