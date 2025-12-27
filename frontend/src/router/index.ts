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
    meta: { layout: 'default' },
    children: [
      {
        path: "/",
        name: "home",
        component: () => import('../pages/e-commerce/Home/Home.vue')
      },
      {
        path: "/products/:slug",
        name: "products",
        component: () => import('../pages/e-commerce/Product/Products.vue')
      },
      {
        path: "/profile",
        name: "profile",
        component: () => import('../pages/e-commerce/Profile/Profile.vue'),
        meta: { requiresAuth: true, role: RoleEnum.USER }
      },

      {
        path: "/cart",
        name: "cart",
        component: () => import('../pages/e-commerce/Cart/Cart.vue'),
        meta: { requiresAuth: true }
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
        name: "admin-statistics",
        component: () => import('../pages/admin/Dashboard.vue')
      },
      {
        path: "products",
        name: "admin-products",
        component: () => import('../pages/admin/Product/ProductList.vue')
      },
      {
        path: "categories",
        name: "admin-categories",
        component: () => import('../pages/admin/Category/CategoryList.vue')
      },
      {
        path: "orders",
        name: "admin-orders",
        component: () => import('../pages/admin/Order/OrderList.vue')
      },
      {
        path: "customers",
        name: "admin-customers",
        component: () => import('../pages/admin/User/UserList.vue')
      },
      {
        path: "sizes",
        name: "admin-sizes",
        component: () => import('../pages/admin/Size/SizeList.vue')
      },
      {
        path: "colors",
        name: "admin-colors",
        component: () => import('../pages/admin/Color/ColorList.vue')
      },
    ]
  },

  // -------------------- CHAT ROUTES --------------------
  {
    path: "/chats",
    meta: { requiresAuth: true, layout: "chat"},
    children: [
      {
        path: "conversations",
        name: "conversations",
        component: () => import('../pages/chat/Conversation/index.vue')
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
      return { name: "admin-statistics" }
    }
  }

  // 4. Safety: admin path but not admin
  if (to.path.startsWith("/dashboard") && user.value?.role !== RoleEnum.ADMIN) {
    return { name: "home" };
  }

  // 5. Safety: user path but not user
  if (to.path == "/" && user.value?.role == RoleEnum.ADMIN) {
    return { name: "admin-statistics" };
  }
});

export default router;
