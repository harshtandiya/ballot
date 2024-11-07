<template>
  <button
    class="flex divide-x-2 border rounded-sm hover:bg-gray-50 text-sm font-medium group transition-all ease-in-out duration-500"
    :class="
      alreadyLiked.data
        ? 'bg-red-600 text-white hover:bg-red-700 border-red-800 divide-red-800'
        : ''
    "
    @click="handleLike()"
  >
    <div class="flex gap-1 py-2 px-4 items-center">
      <IconHeart
        size="1rem"
        stroke="2"
        class="group-hover:stroke-red-500"
        :class="alreadyLiked.data ? 'fill-white group-hover:stroke-white' : ''"
      />
      <span v-if="alreadyLiked.data">Liked</span>
      <span v-else>Like</span>
    </div>
    <div class="p-2 min-w-12 gap-1 flex items-center justify-center">
      <span>{{ likeCount.data }}</span>
    </div>
  </button>
</template>
<script setup>
import { inject } from 'vue'
import { checkAlreadyLiked, getLikeCount, toggleLike } from '@/utils/like'
import { IconHeart } from '@tabler/icons-vue'

const session = inject('$session')
const props = defineProps({
  referenceDoctype: {
    type: String,
    required: true,
  },
  referenceName: {
    type: String,
    required: true,
  },
})

const alreadyLiked = checkAlreadyLiked(
  props.referenceDoctype,
  props.referenceName,
  session.user,
)

const likeCount = getLikeCount(props.referenceDoctype, props.referenceName)

const handleLike = () => {
  const like = toggleLike(
    props.referenceDoctype,
    props.referenceName,
    session.user,
  )
  like.fetch().then(() => {
    likeCount.fetch()
    alreadyLiked.fetch()
  })
}
</script>
