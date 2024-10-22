<template>
  <Header />
  <div class="w-full flex justify-center">
    <div class="max-w-screen-xl w-full h-screen flex flex-col p-4">
      <div v-if="formDetails.loading">
        <LoadingText />
      </div>
      <div v-if="formDetails.data" class="space-y-4">
        <Breadcrumb class="!pl-0" :items="breadcrumbItems" />
        <div class="flex flex-col gap-3 items-start">
          <Avatar
            v-if="formDetails.data.photo"
            :image="formDetails.data.photo"
            size="xlarge"
          />
          <Avatar
            v-else
            :label="formDetails.data.full_name.charAt(0)"
            size="xlarge"
          />
          <div class="flex flex-col gap-1">
            <h2 class="text-2xl font-semibold">
              {{ formDetails.data.full_name }}
            </h2>
            <div class="text-base">
              {{ formDetails.data.designation }} at
              {{ formDetails.data.organization }}
            </div>
          </div>
          <div class="my-2 space-y-4 w-full">
            <RenderFieldData
              v-for="field in fields_meta"
              :key="field.fieldname"
              :field="field"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import Breadcrumb from '@/components/Breadcrumb.vue'
import Avatar from 'primevue/avatar'
import Header from '@/components/Header.vue'
import RenderFieldData from '@/components/candidature/RenderFieldData.vue'
import { createResource, LoadingText } from 'frappe-ui'
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const breadcrumbItems = ref([
  {
    label: 'Election',
  },
  {
    label: '',
    route: '',
  },
  {
    label: 'Candidates',
  },
])

const fields_meta = ref([])

const election = createResource({
  url: 'ballot.api.election.get_election_from_slug',
  makeParams() {
    return {
      slug: route.params.slug,
    }
  },
  auto: true,
  onSuccess(data) {
    breadcrumbItems.value[1]['label'] = data.title
    breadcrumbItems.value[1]['route'] = `/election/${data.slug}`
  },
})

const formDetails = createResource({
  url: 'ballot.api.candidate.get_candidate_details',
  makeParams() {
    return {
      candidate: route.params.id,
    }
  },
  auto: true,
  onSuccess(data) {
    breadcrumbItems.value.push({ label: data.full_name })
    fields_meta.value = JSON.parse(data.submission_meta).filter(
      (field) =>
        field.fieldtype !== 'Section Break' &&
        field.fieldtype !== 'Column Break',
    )
  },
})
</script>
