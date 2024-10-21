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
      {
        path: 'elections',
        name: 'All Elections',
        component: () => import('@/pages/AllElections.vue'),
      },
    ],
  },
  {
    path: '/my-team/:id',
    name: 'Team Dashboard',
    component: () => import('@/pages/TeamDashboard.vue'),
    children: [
      {
        path: '',
        name: 'Team Details',
        component: () => import('@/pages/team/Details.vue'),
      },
      {
        path: 'elections',
        name: 'Team Elections',
        component: () => import('@/pages/team/Elections.vue'),
      },
    ],
  },
  {
    path: '/my-elections/:id',
    name: 'Election Dashboard',
    component: () => import('@/pages/election/ElectionDashboard.vue'),
    children: [
      {
        path: '',
        name: 'Election Details',
        component: () => import('@/pages/election/Details.vue'),
      },
      {
        path: 'nomination',
        name: 'Nomination Dashboard',
        component: () => import('@/pages/election/NominationFormDashboard.vue'),
      },
    ],
  },
  {
    path: '/create-nomination-form',
    name: 'Create Nomination Form',
    component: () => import('@/pages/election/CreateNominationForm.vue'),
    beforeEnter: (to, from, next) => {
      if (!to.query.election) {
        next(false)
        router.replace({
          name: 'ErrorPage',
          params: { missingParam: 'election' },
        })
      } else {
        next()
      }
    },
  },
  {
    path: '/manage-candidate-form/:id',
    name: 'Manage Candidate Form',
    component: () => import('@/pages/election/ManageNominationForm.vue'),
  },
  {
    path: '/error',
    name: 'ErrorPage',
    component: () => import('@/pages/ErrorPage.vue'),
    props: true,
  },
  {
    path: '/election/:slug',
    name: 'Election Public Page',
    component: () => import('@/pages/election/ElectionHome.vue'),
    meta: { isPublicPage: true },
  },
  {
    path: '/election/:slug/apply',
    name: 'Nomination Form',
    component: () => import('@/pages/election/CandidatureFormPublic.vue'),
    meta: { isPublicPage: true },
  },
  {
    path: '/my-submissions',
    name: 'My Submissions',
    component: () => import('@/pages/submissions/MySubmissions.vue'),
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
