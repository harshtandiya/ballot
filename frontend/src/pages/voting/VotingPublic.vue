<template>
  <Header />
  <ConfirmationDialog
    v-model:show="showConfirmationModal"
    :candidates="selectedCandidates"
    @confirm-vote="submitVote()"
  />
  <div class="w-full flex justify-center">
    <div v-if="election.loading">
      <LoadingIndicator />
    </div>
    <div
      v-if="election.data"
      class="max-w-screen-xl w-full h-screen flex flex-col p-4"
    >
      <Breadcrumb :items="breadcrumb_items" class="!px-0" />
      <div class="space-y-2 my-3">
        <Badge
          :label="`Voting is ${election.data?.voting_status}`"
          size="lg"
          variant="outline"
          :theme="election.data?.voting_status == 'Live' ? 'green' : 'gray'"
        >
          <template v-if="election.data?.voting_status == 'Live'" #prefix>
            <LivePing />
          </template>
        </Badge>
        <h1 class="text-3xl font-bold">{{ election.data?.title }}</h1>
        <div
          class="text-base &>*[!p-0]"
          v-html="election.data?.vote_page_description"
        ></div>
      </div>
      <hr class="my-3" />
      <div v-if="election.data?.voting_status == 'Live' && !hasVoted">
        <h3 class="text-lg my-2">
          Please select
          <span class="font-semibold">
            {{ election.data?.allowed_preference_count }}
          </span>
          candidates of your choice
        </h3>
        <!-- Candidate Selection Area -->
        <div
          v-if="allCandidates.data"
          class="flex flex-col gap-4 p-4 w-full justify-center items-center bg-gray-100 border rounded"
        >
          <div
            v-for="(candidate, index) in selectedCandidates"
            :key="index"
            class="flex gap-2 items-center mx-auto"
          >
            <div
              class="flex text-center justify-center items-center w-10 h-10 text-base bg-white rounded border border-gray-400"
            >
              {{ index + 1 }}
            </div>
            <div>
              <CandidatePreviewCard
                v-if="candidate.name"
                :candidate="candidate"
              />
              <div v-else>
                <Select
                  v-model="selectedCandidates[index]"
                  :options="availableCandidates"
                  placeholder="Select a candidate"
                >
                  <template #option="slotProps">
                    <div class="flex gap-3 items-start">
                      <Avatar
                        v-if="slotProps.option.photo"
                        :image="slotProps.optionphoto"
                      />
                      <Avatar
                        v-else
                        :label="slotProps.option.full_name.charAt(0)"
                      />
                      <div class="flex flex-col gap-1">
                        <h5 class="text-lg font-medium">
                          {{ slotProps.option.full_name }}
                        </h5>
                        <div class="text-sm">
                          {{ slotProps.option.designation }} at
                          {{ slotProps.option.organization }}
                        </div>
                      </div>
                    </div>
                  </template>
                </Select>
              </div>
            </div>
            <Button
              v-if="candidate.name"
              icon="trash"
              variant="solid"
              theme="red"
              @click="removeSelectedCandidate(index)"
            />
          </div>
        </div>
        <!-- End of Candidate Selection Area -->
        <div class="w-full flex justify-end my-4">
          <Button
            label="Submit"
            variant="solid"
            size="lg"
            :disabled="!validateSelectedCandidates()"
            @click="showConfirmationModal = true"
          />
        </div>
      </div>
      <div v-else>
        <div class="m-auto p-4 gap-2 flex flex-col items-center justify-center">
          <IconCircleOff />
          <h3 v-if="hasVoted">You have already voted for this election</h3>
          <h3 v-else class="text-lg my-2">
            Voting is {{ election.data?.voting_status }}. Stay tuned for
            updates!
          </h3>
        </div>
      </div>
      <ErrorMessage :message="errorMessages" />
    </div>
  </div>
</template>
<script setup>
import { IconCircleOff } from '@tabler/icons-vue'
import { computed, inject, ref } from 'vue'
import {
  createResource,
  Badge,
  ErrorMessage,
  LoadingIndicator,
} from 'frappe-ui'
import { toast } from 'vue-sonner'
import { useRoute } from 'vue-router'
import LivePing from '@/components/animations/LivePing.vue'
import Header from '@/components/Header.vue'
import Breadcrumb from '@/components/Breadcrumb.vue'
import Select from 'primevue/select'
import Avatar from 'primevue/avatar'
import CandidatePreviewCard from '@/components/voting/CandidatePreviewCard.vue'
import ConfirmationDialog from '@/components/voting/ConfirmationDialog.vue'

const route = useRoute()
const session = inject('$session')

const errorMessages = ref('')

const selectedCandidates = ref([])

const showConfirmationModal = ref(false)

const election = createResource({
  url: 'ballot.api.election.get_election_from_slug',
  makeParams() {
    return {
      slug: route.params.slug,
    }
  },
  auto: true,
  onSuccess(data) {
    allCandidates.fetch()
    hasVoted.fetch()
    for (let i = 0; i < data.allowed_preference_count; i++) {
      selectedCandidates.value.push({})
    }
  },
})

const breadcrumb_items = computed(() => {
  return [
    {
      label: election.data?.title,
      route: `/election/${route.params.slug}`,
    },
    {
      label: 'Voting',
    },
  ]
})

const allCandidates = createResource({
  url: 'ballot.api.candidate.get_candidate_list_for_voting',
  makeParams() {
    return {
      election: election.data?.name,
    }
  },
})

const availableCandidates = computed(() => {
  return (
    allCandidates.data?.filter((candidate) => {
      return !selectedCandidates.value.some(
        (selected) => selected.name === candidate.name,
      )
    }) || []
  )
})

const hasVoted = createResource({
  url: 'frappe.client.get_count',
  makeParams() {
    return {
      doctype: 'Candidate Vote',
      filters: {
        vote_by: session.user,
        election: election.data?.name,
      },
    }
  },
})

const validateSelectedCandidates = () => {
  return selectedCandidates.value.every((candidate) => {
    return candidate.name
  })
}

const removeSelectedCandidate = (index) => {
  selectedCandidates.value[index] = {}
}

const submitVote = () => {
  const errors = []

  if (!validateSelectedCandidates()) {
    errors.push('Please select at least one candidate')
  }

  // Extra validations
  if (
    selectedCandidates.value.length < election.data?.allowed_preference_count
  ) {
    errors.push(
      `Please select exactly ${election.data?.allowed_preference_count} candidates`,
    )
  }

  if (
    new Set(selectedCandidates.value.map((candidate) => candidate.name))
      .size !== selectedCandidates.value.length
  ) {
    errors.push('Duplicate candidates selected')
  }

  if (errors.length) {
    errorMessages.value = errors.join('\n')
    return
  }

  errorMessages.value = ''

  let _candidate_tiers = formatVotes(selectedCandidates.value)

  createResource({
    url: 'frappe.client.submit',
    makeParams() {
      return {
        doc: {
          doctype: 'Candidate Vote',
          vote_by: session.user,
          election: election.data?.name,
          candidate_tiers: _candidate_tiers,
        },
      }
    },
    onSuccess(data) {
      showConfirmationModal.value = false
      election.fetch()
      toast.success('Vote submitted successfully!')
    },
    onError(err) {
      errorMessages.value = err.message
      toast.error('Error submitting vote')
    },
    auto: true,
  })
}

const formatVotes = (candidates) => {
  let _candidates = []

  for (let i = 0; i < candidates.length; i++) {
    _candidates.push({
      candidate: candidates[i].candidate_id,
      rank: i + 1,
    })
  }

  return _candidates
}
</script>
