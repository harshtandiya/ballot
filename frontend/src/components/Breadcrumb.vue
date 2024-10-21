<template>
  <Breadcrumb :model="items">
    <template #item="{ item, props }">
      <router-link
        v-if="item.route"
        v-slot="{ href, navigate }"
        :to="item.route"
        custom
      >
        <a :href="href" v-bind="props.action" @click="navigate">
          <span
            class="text-primary-600 text-base transition-colors hover:text-primary-800 font-medium"
            >{{ item.label }}</span
          >
        </a>
      </router-link>
      <a v-else :href="item.url" :target="item.target" v-bind="props.action">
        <span class="text-primary-700 text-base font-medium">{{
          item.label
        }}</span>
      </a>
    </template>
    <template #separator>
      <IconChevronRight class="text-primary-600" size="1.5rem" />
    </template>
  </Breadcrumb>
</template>
<script setup>
import Breadcrumb from 'primevue/breadcrumb'
import { IconChevronRight } from '@tabler/icons-vue'

defineProps({
  items: {
    type: Object,
    required: true,
  },
})
</script>
