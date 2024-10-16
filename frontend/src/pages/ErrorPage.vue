<template>
  <div class="w-full h-screen flex flex-col gap-4 items-center justify-center">
    <h2 class="text-lg font-sans font-bold">Ballot.</h2>
    <h1 class="text-xl font-semibold">Oops! Something Went Wrong</h1>
    <p v-if="missingParams">The route is missing some query params.</p>
    <Button label="Go Home" variant="solid" route="/"></Button>
  </div>
</template>
<script setup>
defineProps({
  missingParams: {
    type: String,
    default: '',
  },
})
</script>
