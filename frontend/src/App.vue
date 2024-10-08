<template>
  <div>
    <router-view />
    <Toaster rich-colors />
  </div>
</template>
<script setup>
import { Toaster } from 'vue-sonner'
import { session } from '@/data/session'
import { provide } from 'vue'

provide('$session', session)
</script>
