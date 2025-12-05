import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('../pages/index.vue'),
    meta: { layout: "default" }
  },
  {
    path: '/signin',
    component: () => import('../pages/auth/signin.vue'),
    meta: { layout: "auth" }
  },
  {
    path: '/signup',
    component: () => import('../pages/auth/signup.vue'),
    meta: { layout: "auth" }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../pages/NotFound.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
