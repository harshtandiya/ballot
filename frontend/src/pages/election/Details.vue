<template>
  <div
    v-if="election.loading"
    class="p-5 flex items-center justify-center h-screen w-full"
  >
    <LoadingText />
  </div>
  <div v-if="election.data" class="p-4 flex flex-col gap-4">
    <div class="border-b">
      <h3 class="text-sm uppercase font-medium text-primary-600">
        Election Details
      </h3>
      <h1 class="mt-2 mb-4 text-3xl font-semibold font-sans">
        {{ election.data.title }}
      </h1>
    </div>
    <div class="my-4 space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <FloatLabel variant="on">
          <Select
            id="status"
            v-model="details.status"
            :options="['Draft', 'Live', 'Cancelled', 'Concluded']"
            class="w-full"
          ></Select>
          <label for="status">Status</label>
        </FloatLabel>
        <div class="space-y-1">
          <FloatLabel variant="on">
            <InputText
              id="slug"
              v-model="details.slug"
              class="w-full"
              :invalid="invalidSlug.invalid"
              @input="checkSlugValidity.fetch()"
            ></InputText>
            <label for="slug">Slug</label>
          </FloatLabel>
          <ErrorMessage :message="invalidSlug.message" />
        </div>
        <FloatLabel variant="on">
          <InputText
            id="title"
            v-model="details.title"
            class="w-full"
          ></InputText>
          <label for="title">Title</label>
        </FloatLabel>
        <div class="col-span-2 space-y-1">
          <label
            for="description"
            class="text-sm tracking-tight font-medium text-primary-500"
          >
            Description
          </label>
          <Editor
            id="description"
            v-model="details.description"
            placeholder="Write a detailed description about this election."
            editor-style="height: 320px"
          />
        </div>
      </div>
      <ErrorMessage :message="errorMessages" />
      <Button
        label="Update"
        variant="solid"
        class="w-full md:w-1/4"
        @click="handleSave()"
      />
    </div>
  </div>
</template>
<script setup>
import { createResource, ErrorMessage, LoadingText } from 'frappe-ui'
import { useRoute } from 'vue-router'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import Editor from 'primevue/editor'
import { reactive, ref } from 'vue'
import { toast } from 'vue-sonner'

const route = useRoute()
const errorMessages = ref('')

const invalidSlug = reactive({
  invalid: false,
  message: '',
})

const checkSlugValidity = createResource({
  url: 'ballot.utils.is_slug_valid',
  makeParams() {
    return {
      doctype: 'Election',
      slug: details.slug,
      docname: route.params.id,
    }
  },
  onSuccess(data) {
    if (!data) {
      invalidSlug.invalid = true
      invalidSlug.message = 'This slug is not available'
      return
    }
    invalidSlug.invalid = false
    invalidSlug.message = ''
  },
})

// Fix needed for Quill v2: https://github.com/primefaces/primevue/issues/5606#issuecomment-2203975395
Editor.methods.renderValue = function renderValue(value) {
  if (this.quill) {
    if (value) {
      const delta = this.quill.clipboard.convert({ html: value })
      this.quill.setContents(delta, 'silent')
    } else {
      this.quill.setText('')
    }
  }
}

const details = reactive({
  title: '',
  description: '',
  status: '',
  slug: '',
})

const election = createResource({
  url: 'frappe.client.get',
  makeParams() {
    return {
      doctype: 'Election',
      name: route.params.id,
    }
  },
  auto: true,
  loading: true,
  onSuccess(data) {
    details.title = data.title
    details.description = data.description
    details.status = data.status
    details.slug = data.slug
  },
})

const saveDetails = createResource({
  url: 'frappe.client.set_value',
  makeParams() {
    return {
      doctype: 'Election',
      name: route.params.id,
      fieldname: {
        title: details.election,
        description: details.description,
        status: details.status,
        slug: details.slug,
      },
    }
  },
  onSuccess() {
    errorMessages.value = ''
    toast.success('Details Update')
  },
  onError(err) {
    toast.error('Failed to update details')
    errorMessages.value = err.messages
  },
})

const handleSave = () => {
  const errors = []
  if (invalidSlug.invalid) {
    errors.push('Unique slug is required')
  }

  if (errors.length) {
    errorMessages.value = errors.join('\n')
    return
  }

  saveDetails.fetch()
}
</script>
