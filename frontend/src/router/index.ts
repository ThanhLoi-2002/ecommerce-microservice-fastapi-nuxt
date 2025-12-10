import { useUserStore } from '@/stores/user.store';
import { RoleEnum } from '@/types/entities';
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
        path: "",
        name: "dashboard",
        component: () => import('../pages/admin/Dashboard.vue')
      },
      {
        path: "products",
        name: "products",
        component: () => import('../pages/admin/Dashboard.vue')
      },
      {
        path: "orders",
        name: "orders",
        component: () => import('../pages/admin/Dashboard.vue')
      },
      {
        path: "customers",
        name: "customers",
        component: () => import('../pages/admin/Dashboard.vue')
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
  const userStore = useUserStore();
  const { isAuth, user } = storeToRefs(userStore);
  const token = getToken();

  // 👉 Nếu có token và chưa login thì load user info
  if (token && !isAuth.value) {
    await userStore.getMeHandler();
  }

  // 1. Guest only (signin/signup)
  if (to.meta.guestOnly && isAuth.value) {
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
      return { name: "dashboard" }
    }
  }

  // 4. Safety: admin path but not admin
  if (to.path.startsWith("/dashboard") && user.value?.role !== RoleEnum.ADMIN) {
    return { name: "home" };
  }
});

export default router;
