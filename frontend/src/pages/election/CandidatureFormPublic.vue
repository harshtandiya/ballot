<template>
  <Header />
  <div class="flex w-full justify-center py-6">
    <div class="space-y-4 w-full max-w-screen-xl px-6">
      <h1 class="text-3xl font-sans font-semibold">Apply for Nomination</h1>
      <Divider />
      <div v-if="form.loading">
        <LoadingText />
      </div>
      <RenderForm
        v-else
        v-model:fields="fields_meta"
        :election="election.data"
        :form="form.data"
      ></RenderForm>
    </div>
  </div>
</template>
<script setup>
import Header from '@/components/Header.vue'
import Divider from 'primevue/divider'
import { createResource, LoadingText } from 'frappe-ui'
import { useRoute } from 'vue-router'
import RenderForm from '@/components/form/RenderForm.vue'
import { ref } from 'vue'

const route = useRoute()

const fields_meta = ref([])

const election = createResource({
  url: 'frappe.client.get',
  makeParams() {
    return {
      doctype: 'Election',
      filters: {
        slug: route.params.slug,
      },
    }
  },
  auto: true,
  onSuccess() {
    form.fetch()
  },
})

const form = createResource({
  url: 'frappe.client.get',
  makeParams() {
    return {
      doctype: 'Election Nomination Form',
      filters: {
        election: election.data.name,
      },
    }
  },
  loading: true,
  onSuccess(data) {
    fields_meta.value = JSON.parse(data.fields_meta)
  },
})
</script>
