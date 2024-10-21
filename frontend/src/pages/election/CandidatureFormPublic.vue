<template>
  <Header />
  <div class="flex w-full justify-center py-4">
    <div class="space-y-4 w-full max-w-screen-xl px-6">
      <div v-if="formStatus == 'Loading'">
        <LoadingText />
      </div>
      <div v-else-if="formStatus == 'Live'">
        <Breadcrumb class="mb-2 !pl-0" :items="breadcrumbItems" />
        <h1 class="text-3xl font-sans font-semibold">Apply for Candidature</h1>
        <Divider />
        <div class="mt-2 mb-4" v-html="form.data.description"></div>
        <div>
          <RenderForm
            v-model:fields="fields_meta"
            :election="election.data"
            :form="form.data"
          ></RenderForm>
        </div>
      </div>
      <div v-else>
        <div
          class="w-full h-[320px] flex gap-2 flex-col justify-center items-center"
        >
          <IconAlertCircle size="2rem" />
          <h1 class="text-xl font-semibold">
            This candidature form is not live!
          </h1>
          <p class="text-base text-primary-600">
            Please contact organizing team members for more info.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import Header from '@/components/Header.vue'
import Divider from 'primevue/divider'
import Breadcrumb from '@/components/Breadcrumb.vue'
import { createResource, LoadingText } from 'frappe-ui'
import { useRoute } from 'vue-router'
import RenderForm from '@/components/form/RenderForm.vue'
import { ref } from 'vue'
import { IconAlertCircle } from '@tabler/icons-vue'

const route = useRoute()
const formStatus = ref('Loading')
const fields_meta = ref([])
const breadcrumbItems = ref([
  {
    label: 'Elections',
  },
])

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
  onSuccess(data) {
    breadcrumbItems.value.push({
      label: data.title,
      route: `/election/${data.slug}`,
    })
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
    breadcrumbItems.value.push({ label: 'Candidate Form' })
    formStatus.value = data.status
    if (data.status === 'Live') {
      fields_meta.value = JSON.parse(data.fields_meta)
    }
  },
})
</script>
