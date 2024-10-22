<template>
  <div
    v-for="comment in comments.data"
    :key="comment.name"
    class="flex flex-col py-2 w-full"
  >
    <RenderComment :comment="comment" @refresh-comments="reloadComments" />
  </div>
</template>
<script setup>
import { createResource } from 'frappe-ui'
import RenderComment from './RenderComment.vue'

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

const comments = createResource({
  url: 'ballot.api.comments.get_all_comments',
  makeParams() {
    return {
      doctype: props.doctype,
      docname: props.docname,
    }
  },
  auto: true,
})

const reloadComments = () => {
  comments.fetch()
}

defineExpose({ reloadComments })
</script>
