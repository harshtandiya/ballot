import { createRouter, createWebHistory } from 'vue-router'
import { session } from './data/session'
import { userResource } from '@/data/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    redirect: { name: 'Dashboard' },
    component: () => import('@/pages/Home.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/pages/Dashboard.vue'),
      },
    ],
  },
  {
    path: '/myteam/:id',
    name: 'Team Dashboard',
    component: () => import('@/pages/TeamDashboard.vue'),
    children: [
      {
        path: '',
        name: 'Team Details',
        component: () => import('@/pages/team/Details.vue'),
      },
    ],
  },
]

let router = createRouter({
  history: createWebHistory('/ballot'),
  routes,
})

router.beforeEach(async (to, from, next) => {
  let isLoggedIn = session.isLoggedIn
  try {
    await userResource.promise
  } catch (error) {
    isLoggedIn = false
  }

  if (to.name === 'Login' && isLoggedIn) {
    next({ name: 'Home' })
  } else if (to.name !== 'Login' && !isLoggedIn && !to.meta.isPublicPage) {
    window.location.href = `/login?redirect-to=/ballot${to.fullPath}`
  } else {
    next()
  }
})

export default router
