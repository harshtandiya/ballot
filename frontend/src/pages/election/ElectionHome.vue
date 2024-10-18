<template>
  <Header />
  <div class="w-full flex justify-center">
    <div
      v-if="election.data"
      class="max-w-screen-xl w-full h-screen flex flex-col p-4"
    >
      <div class="space-y-2 my-3">
        <h3 class="text-sm uppercase text-primary-600">Election</h3>
        <h1 class="text-3xl font-bold">
          {{ election.data.title }}
        </h1>
        <div v-html="election.data.description"></div>
      </div>
      <hr />
      <div class="w-full grid grid-cols-1 md:grid-cols-2">
        <div v-if="hasCandidateForm.loading"></div>
        <CandidateFormStatusBanner
          v-else-if="hasCandidateForm.data && candidateForm.data"
          class="my-4"
          :has-form="hasCandidateForm.data"
          :form="candidateForm.data"
        />
        <CandidateFormStatusBanner
          v-else
          class="my-4"
          :has-form="hasCandidateForm.data"
        />
      </div>
    </div>
  </div>
</template>
<script setup>
import Header from '@/components/Header.vue'
import CandidateFormStatusBanner from './CandidateFormStatusBanner.vue'
import { createResource } from 'frappe-ui'
import { useRoute } from 'vue-router'

const route = useRoute()

const election = createResource({
  url: 'ballot.api.election.get_election_from_slug',
  makeParams() {
    return {
      slug: route.params.slug,
    }
  },
  auto: true,
  onSuccess() {
    hasCandidateForm.fetch()
  },
})

const hasCandidateForm = createResource({
  url: 'ballot.api.election.has_nomination_form',
  makeParams() {
    return {
      election: election.data.name,
    }
  },
  loading: true,
  onSuccess(data) {
    if (!data) {
      return
    }
    candidateForm.fetch()
  },
})

const candidateForm = createResource({
  url: 'ballot.api.election.get_election_candidature_form',
  makeParams() {
    return {
      election: election.data.name,
    }
  },
})
</script>
