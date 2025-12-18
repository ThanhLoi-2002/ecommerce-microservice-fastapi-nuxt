import { useUser } from '@/composables/useUser';
import { useAuthStore } from '@/stores/auth.store';
import { useUserStore } from '@/stores/user.store';
import { RoleEnum } from '@/types/common';
import { getToken } from '@/utils/token';
import { storeToRefs } from 'pinia';
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  // -------------------- AUTH ROUTES --------------------
  {
    path: "/auth",
    meta: { layout: "auth" },
    children: [
      {
        path: "signin",
        name: "signin",
        component: () => import('../pages/auth/signin.vue'),
        meta: { guestOnly: true }
      },
      {
        path: "signup",
        name: "signup",
        component: () => import('../pages/auth/signup.vue'),
        meta: { guestOnly: true }
      }
    ]
  },

  // -------------------- USER ROUTES --------------------
  {
    path: "",
    meta: { role: RoleEnum.USER, layout: 'default' },
    children: [
      {
        path: "/",
        name: "home",
        component: () => import('../pages/e-commerce/Home/Home.vue')
      },
      {
        path: "/profile",
        name: "profile",
        component: () => import('../pages/e-commerce/Profile/Profile.vue'),
        meta: { requiresAuth: true, role: RoleEnum.USER }
      },
    ]
  },

  // -------------------- ADMIN ROUTES --------------------
  {
    path: "/dashboard",
    meta: { layout: "admin", requiresAuth: true, role: RoleEnum.ADMIN },
    children: [
      {
        path: "statistics",
        name: "statistics",
        component: () => import('../pages/admin/Dashboard.vue')
      },
      {
        path: "products",
        name: "products",
        component: () => import('../pages/admin/Product/ProductList.vue')
      },
      {
        path: "categories",
        name: "categories",
        component: () => import('../pages/admin/Category/CategoryList.vue')
      },
      {
        path: "orders",
        name: "orders",
        component: () => import('../pages/admin/Order/OrderList.vue')
      },
      {
        path: "customers",
        name: "customers",
        component: () => import('../pages/admin/User/UserList.vue')
      },
    ]
  },

  // -------------------- 404 --------------------
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../pages/NotFound.vue'),
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// -------------------- GLOBAL GUARD --------------------
router.beforeEach(async (to) => {
  const authStore = useAuthStore();
  const { isAuth } = storeToRefs(authStore);
  const userStore = useUserStore()
  const { user } = storeToRefs(userStore)
  const token = getToken()
  const { getMe } = useUser()

  if (token && !isAuth.value) {
    await getMe();
  }

  // 1. Guest only (signin/signup)
  if (to.meta.guestOnly && isAuth.value) {
    console.log("kick")
    return { name: "home" };
  }

  // 2. Requires login
  if (to.meta.requiresAuth && !isAuth.value) {
    return { name: "signin" };
  }

  // 3. Role check
  if (to.meta.role) {
    const requiredRole = to.meta.role;

    if (user.value?.role == RoleEnum.ADMIN && requiredRole == RoleEnum.USER) {
      return { name: "statistics" }
    }
  }

  // 4. Safety: admin path but not admin
  if (to.path.startsWith("/dashboard") && user.value?.role !== RoleEnum.ADMIN) {
    return { name: "home" };
  }
});

export default router;
