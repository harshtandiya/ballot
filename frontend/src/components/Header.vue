<template>
  <div class="w-full px-5 py-3 border-b flex justify-between">
    <h2 class="text-2xl font-sans font-bold">Ballot.</h2>
    <a
      href="/ballot"
      class="text-base flex items-center gap-1 text-primary-800 hover:text-primary-600 hover:cursor-pointer"
    >
      Go to ballot dashboard <IconArrowRight size="1rem" />
    </a>
  </div>
</template>
<script setup>
import { IconArrowRight } from '@tabler/icons-vue'
</script>
