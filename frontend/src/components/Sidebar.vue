<template>
  <div
    class="relative block min-h-0 flex-shrink-0 overflow-hidden hover:overflow-auto"
  >
    <div
      class="fixed flex justify-between min-h-screen w-[220px] flex-col border-r bg-primary-50 p-4"
    >
      <div class="flex flex-col gap-4">
        <slot name="branding">
          <div class="mb-3">
            <div class="font-sans text-2xl font-semibold">Ballot.</div>
          </div>
        </slot>
        <slot name="pre-nav-items"></slot>
        <slot name="nav-items">
          <div class="flex flex-col gap-1">
            <Button
              v-for="(item, index) in sidebarItems"
              :key="item.label"
              :label="item.label"
              :variant="
                isMenuItemActive(item.route, index) ? 'subtle' : 'ghost'
              "
              :class="
                isMenuItemActive(item.route, index)
                  ? 'bg-gray-200 font-medium'
                  : ''
              "
              size="sm"
              class="!justify-start text-sm rounded-sm"
              @click="router.push(item.route)"
            />
          </div>
        </slot>
        <slot name="post-nav-items"></slot>
      </div>
      <slot name="user-actions">
        <div class="flex flex-col gap-4">
          <div class="flex items-center justify-between text-gray-800">
            <div class="flex items-center gap-2">
              <img
                v-if="userDetails.data?.user_image"
                :src="userDetails.data?.user_image"
                class="w-6 h-6 rounded-full"
              />
              <IconUserFilled v-else class="w-3 h-3" />
              <span class="text-sm font-medium">{{
                userDetails.data?.full_name
              }}</span>
            </div>
            <div>
              <Popover>
                <template #target="{ togglePopover }">
                  <Button
                    icon="more-vertical"
                    variant="ghost"
                    @click="togglePopover()"
                  />
                </template>
                <template #body-main>
                  <div class="flex flex-col gap-1 p-2">
                    <Button
                      class="!justify-start text-sm rounded-sm cursor-pointer"
                      label="My Profile"
                      :link="getRedirectUrl('me')"
                      variant="ghost"
                    />
                    <Button
                      variant="ghost"
                      theme="red"
                      class="!justify-start text-sm rounded-sm cursor-pointer"
                      label="Logout"
                      @click="session.logout.fetch()"
                    />
                  </div>
                </template>
              </Popover>
            </div>
          </div>
        </div>
      </slot>
    </div>
  </div>
</template>
<script setup>
import { IconUserFilled } from '@tabler/icons-vue'
import { createResource, Popover } from 'frappe-ui'
import { inject } from 'vue'
import { getRedirectUrl } from '@/utils/helpers'
import { useRoute, useRouter } from 'vue-router'

const session = inject('$session')
const route = useRoute()
const router = useRouter()

const props = defineProps({
  sidebarItems: {
    type: Array,
    default() {
      return []
    },
  },
})

const userDetails = createResource({
  url: 'ballot.api.user.get_user_details',
  makeParams() {
    return {
      user: session.user,
    }
  },
  auto: true,
})

const isMenuItemActive = (menuRoute, index) => {
  if (index == 0 && menuRoute != route.path) {
    return false
  }
  return (
    menuRoute === route.path ||
    menuRoute ===
      '/' + route.path.split('/').filter(Boolean).slice(0, -1).join('/')
  )
}
</script>
