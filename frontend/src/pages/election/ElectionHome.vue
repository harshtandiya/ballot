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
        <div
          class="text-base &>*[!p-0]"
          v-html="election.data.description"
        ></div>
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
      <div v-if="candidates.data" class="mt-4 space-y-2">
        <h2 class="text-xl font-semibold">Candidates</h2>
        <hr />
        <p
          v-if="candidates.data.length == 0"
          class="text-base pt-2 text-primary-700"
        >
          No candidates for this election yet.
        </p>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <CandidateCard
            v-for="candidate in candidates.data"
            :key="candidate.name"
            :candidate="candidate"
          />
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import Header from '@/components/Header.vue'
import CandidateFormStatusBanner from '@/components/candidature/CandidateFormStatusBanner.vue'
import CandidateCard from '@/components/candidature/CandidateCard.vue'
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
    candidates.fetch()
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

const candidates = createResource({
  url: 'ballot.api.candidate.get_all_candidates',
  makeParams() {
    return {
      election: election.data.name,
    }
  },
})
</script>
