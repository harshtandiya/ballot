<template>
  <div class="space-y-2 my-5 w-full">
    <div class="space-x-2">
      <h5 class="text-lg font-semibold">Comments</h5>
    </div>
    <p class="text-base text-primary-600">
      Comments will be public and non-anonymous.
    </p>
    <CommentBox
      :doctype="doctype"
      :docname="docname"
      @refresh-comments="refreshCommentsList"
    />
    <CommentsList ref="commentsList" :doctype="doctype" :docname="docname" />
  </div>
</template>
<script setup>
import CommentBox from './CommentBox.vue'
import CommentsList from './CommentsList.vue'
import { ref } from 'vue'

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

const commentsList = ref(null)

const refreshCommentsList = () => {
  if (commentsList.value) {
    commentsList.value.reloadComments()
  }
}
</script>
