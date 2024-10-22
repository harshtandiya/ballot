<template>
  <div class="flex flex-col">
    <div class="flex items-center gap-2">
      <Avatar v-if="comment.user_image" :image="comment.user_image" />
      <Avatar v-else :label="comment.full_name.charAt(0)" />
      <h5 class="text-base font-medium">{{ comment.full_name }}</h5>
      <span class="text-sm font-light">
        {{ getRelativeTime(comment.creation) }}
      </span>
    </div>
    <div class="px-6 ml-4 pt-1 text-base space-y-2 border-l border-gray-500">
      <div class="[&>*]:!p-0" v-html="comment.content"></div>
      <div v-if="session.user != null" class="flex gap-2">
        <Button
          icon-left="corner-up-left"
          label="Reply"
          variant="ghost"
          @click="toggleReply"
        />
      </div>
      <CommentBox
        v-if="showReply"
        doctype="Comment"
        :docname="comment.name"
        @refresh-comments="handleReply"
      />
    </div>
  </div>
  <div v-if="comment.replies.length > 0" class="flex ml-4 w-full">
    <div class="w-5 h-5 rounded-bl border-l border-b border-gray-500"></div>
    <div class="flex flex-col w-full">
      <CommentsList doctype="Comment" :docname="comment.name" />
    </div>
  </div>
</template>
<script setup>
import CommentBox from './CommentBox.vue'
import CommentsList from './CommentsList.vue'
import Avatar from 'primevue/avatar'
import { getRelativeTime } from '@/utils/helpers'
import { inject, ref } from 'vue'

const showReply = ref(false)
const toggleReply = () => {
  showReply.value = !showReply.value
}

const emit = defineEmits(['refresh-comments'])

const session = inject('$session')
const props = defineProps({
  comment: {
    type: Object,
    required: true,
  },
})

const handleReply = () => {
  showReply.value = false
  emit('refresh-comments')
}
</script>
