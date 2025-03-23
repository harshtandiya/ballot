<template>
  <div class="p-4 flex flex-col gap-4">
    <div class="border-b mb-2 pb-4 space-y-2">
      <h3 class="text-sm uppercase font-medium text-primary-600">Manage</h3>
      <div class="flex gap-2 items-center">
        <h1 class="text-3xl font-semibold font-sans">Voting</h1>
        <Badge
          :label="election.data?.voting_status"
          :theme="election.data?.voting_status == 'Live' ? 'green' : 'gray'"
        >
          <template v-if="election.data?.voting_status == 'Live'" #prefix>
            <LivePing />
          </template>
        </Badge>
      </div>
      <p class="text-sm text-primary-600">
        Manage your election voting process
      </p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="flex flex-col gap-2">
        <h4 class="text-base text-primary-600">
          Voting is
          <span class="font-semibold">{{ election.data?.voting_status }}</span>
        </h4>
        <Button
          class="w-fit"
          :label="
            { Live: 'Close', Closed: 'Open' }[election.data?.voting_status]
          "
          :theme="
            { Live: 'red', Closed: 'green' }[election.data?.voting_status]
          "
          @click="toggleVotingStatus.fetch()"
        />
      </div>
      <div class="space-y-2">
        <h4 class="text-base text-primary-600">Voting page link</h4>
        <FormControl :value="getVotingLink()" disabled>
          <template #suffix>
            <CopyToClipboardButton :value-to-copy="getVotingLink()" />
          </template>
        </FormControl>
      </div>
      <hr class="col-span-2" />
      <div class="space-y-1">
        <FloatLabel variant="on">
          <label for="allowed_preference_count">Allowed Preference Count</label>
          <InputText
            id="allowed_preference_count"
            v-model="votingData.allowed_preference_count"
            class="w-full"
          ></InputText>
        </FloatLabel>
        <small class="text-primary-500">
          Refers to the number of candidates that can be selected at the time of
          voting
        </small>
      </div>
      <div class="col-span-2 flex flex-col gap-1">
        <label class="text-base text-primary-600" for="vote_page_description">
          Vote Page Description
        </label>
        <small class="text-primary-500">
          This is the description that will be shown on the voting page
        </small>
        <Editor
          id="vote_page_description"
          v-model="votingData.vote_page_description"
          placeholder="Write a description..."
          editor-style="height: 320px"
        />
      </div>
      <ErrorMessage class="col-span-2" :message="errorMessages" />
      <div></div>
      <Button label="Save" variant="solid" @click="handleSave()" />
    </div>
  </div>
</template>
<script setup>
import { Badge, createResource, FormControl, ErrorMessage } from 'frappe-ui'
import { inject, reactive, ref, watch } from 'vue'
import { toast } from 'vue-sonner'
import CopyToClipboardButton from '@/components/ui/CopyToClipboardButton.vue'
import LivePing from '@/components/animations/LivePing.vue'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import Editor from 'primevue/editor'

const errorMessages = ref('')

const election = inject('$election')

const votingData = reactive({
  allowed_preference_count: 1,
  vote_page_description: '',
})

watch(
  () => election.data,
  (newData) => {
    if (newData) {
      Object.assign(votingData, newData)
    }
  },
)

const toggleVotingStatus = createResource({
  url: 'frappe.client.set_value',
  makeParams() {
    return {
      doctype: 'Election',
      name: election.data?.name,
      fieldname: 'voting_status',
      value: {
        Live: 'Closed',
        Closed: 'Live',
      }[election.data?.voting_status],
    }
  },
  onSuccess() {
    election.fetch()
    toast.info('Voting status toggled')
  },
  onError(err) {
    toast.error('Error toggling voting status' + err.message)
  },
})

const getVotingLink = () => {
  return `${window.location.origin}/ballot/election/${election.data?.slug}/vote`
}

const handleSave = () => {
  const errors = []

  if (isNaN(votingData.allowed_preference_count)) {
    errors.push('Allowed Preference Count must be a number')
  }

  if (votingData.allowed_preference_count < 1) {
    errors.push('Allowed Preference Count must be greater than 0')
  }

  if (errors.length) {
    errorMessages.value = errors.join('\n')
    return
  }

  errorMessages.value = ''

  createResource({
    url: 'frappe.client.set_value',
    makeParams() {
      return {
        doctype: 'Election',
        name: election.data?.name,
        fieldname: {
          allowed_preference_count: votingData.allowed_preference_count,
          vote_page_description: votingData.vote_page_description,
        },
      }
    },
    onSuccess() {
      election.fetch()
      toast.success('Voting Details Updated')
    },
    onError(err) {
      toast.error('Error updating voting details' + err.message)
    },
    auto: true,
  })
}
</script>
