import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('../pages/e-commerce/Home/Home.vue'),
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
    path: '/profile',
    component: () => import('../pages/e-commerce/Profile/Profile.vue'),
    meta: { layout: "default" }
  },
  {
    path: '/admin/dashboard',
    component: () => import('../pages/admin/dashboard.vue'),
    meta: { layout: "admin" }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../pages/NotFound.vue'),
    meta: { layout: "default" }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
