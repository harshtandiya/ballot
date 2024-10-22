<template>
  <div
    v-if="!session.user"
    class="w-full h-28 rounded-lg bg-primary-50 border flex flex-col gap-2 items-center justify-center"
  >
    <h5 class="text-lg font-semibold">Login to comment</h5>
    <Button label="Login" variant="solid" size="md" @click="redirectToLogin" />
  </div>
  <div v-else>
    <div class="space-y-2 pt-2">
      <Editor
        v-model="commentContent"
        placeholder="Add comment..."
        editor-style="height: 150px"
      >
        <template #toolbar>
          <span class="ql-formats">
            <button v-tooltip.bottom="'Bold'" class="ql-bold"></button>
            <button v-tooltip.bottom="'Italic'" class="ql-italic"></button>
            <button
              v-tooltip.bottom="'Underline'"
              class="ql-underline"
            ></button>
            <button v-tooltip.bottom="'Link'" class="ql-link"></button>
          </span>
        </template>
      </Editor>
      <ErrorMessage :message="errorMessages" />
      <Button label="Add Comment" variant="solid" @click="handleComment" />
    </div>
  </div>
</template>
<script setup>
import { inject, ref } from 'vue'
import Editor from 'primevue/editor'
import { createResource, ErrorMessage } from 'frappe-ui'
import { toast } from 'vue-sonner'

const errorMessages = ref('')
const commentContent = ref('')
const session = inject('$session')
const emit = defineEmits(['refresh-comments'])
const model = defineModel({ type: String, required: true })
const props = defineProps({
  doctype: {
    type: String,
    required: true,
  },
  docname: {
    type: String,
    required: true,
  },
})

const redirectToLogin = () => {
  window.location.href = `/login?redirect-to=${window.location.pathname}`
}

const addComment = createResource({
  url: 'ballot.api.comments.add_comment',
  makeParams() {
    return {
      reference_doctype: props.doctype,
      reference_name: props.docname,
      content: commentContent.value,
    }
  },
  onSuccess() {
    toast('Comment added')
    emit('refresh-comments')
    commentContent.value = ''
  },
  onError(err) {
    toast.error('Error while adding comment!')
    errorMessages.value = err.messages
  },
})

const handleComment = () => {
  if (!commentContent.value) {
    errorMessages.value = 'Cannot post a blank comment'
    return
  }

  errorMessages.value = ''
  addComment.fetch()
}
</script>
