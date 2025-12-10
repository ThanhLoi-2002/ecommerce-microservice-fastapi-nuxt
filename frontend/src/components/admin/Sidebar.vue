<template>
    <div class="sidebar position-relative" :class="{ collapsed }">

        <!-- Brand -->
        <h4 class="brand" v-if="!collapsed">Clothify</h4>

        <!-- Active highlight -->
        <div class="active-bg" :style="{ top: activeTop + 'px', width: collapsed ? '50px' : activeWidth }"></div>

        <ul class="nav flex-column">
            <li v-for="(item, i) in menu" :key="item.to" :ref="el => setMenuRef(el, i)" class="nav-item">
                 <router-link class="nav-link d-flex align-items-center" :to="item.to" @click="moveActive(i)">
                    <component :is="item.icon" class="icon" />
                    <span v-if="!collapsed" class="nav-label">{{ item.label }}</span>
                </router-link>
            </li>
        </ul>

    </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from "vue";
import { useRoute } from "vue-router";
import { HomeIcon, ShoppingBagIcon, UserGroupIcon } from "@heroicons/vue/24/outline";
import { TagIcon } from "@heroicons/vue/24/solid";

// Define props
const props = defineProps<{
    collapsed: boolean;
}>();

const menu = [
    { label: "Dashboard", to: "/dashboard", icon: HomeIcon },
    { label: "Products", to: "/dashboard/products", icon: TagIcon },
    { label: "Orders", to: "/dashboard/orders", icon: ShoppingBagIcon },
    { label: "Customers", to: "/dashboard/customers", icon: UserGroupIcon },
];

// refs
const route = useRoute();
const menuRefs = ref<HTMLElement[]>([]);
const activeTop = ref(0);
const activeWidth = ref("100%");

// stable ref setter
function setMenuRef(el: any, index: number) {
    if (el) menuRefs.value[index] = el;
}

// move highlight
function moveActive(index: number) {
    const el = menuRefs.value[index];
    if (el) {
        activeTop.value = el.offsetTop;
        activeWidth.value = `${el.clientWidth}px`; // Match width of active item
    }
}

// set active on load
onMounted(() => {
    nextTick(() => {
        const i = menu.findIndex(x => route.path.startsWith(x.to));
        if (i !== -1) moveActive(i);
        console.log('a')
    });
});
</script>

<style scoped>
.sidebar {
    width: 220px;
    background: #ffeef2;
    border-right: 1px solid #ffd6df;
    min-height: 100vh;
    padding: 20px 15px;
    transition: width 0.25s ease;
    position: relative;
}

.sidebar.collapsed {
    width: 80px;
    /* Maintain consistent collapsing */
}

/* Active highlight bar */
.active-bg {
    position: absolute;
    height: 40px;
    /* Match the height of nav items */
    background: white;
    border-radius: 12px;
    transition: top 0.25s, width 0.25s;
    /* Smooth transitions */
    z-index: 1;
}

/* Nav items */
.nav-item {
    position: relative;
    height: 40px;
    display: flex;
    align-items: center;
    z-index: 2;
}

/* Ensuring label shows correctly */
.nav-label {
    margin-left: 10px;
    /* Space between icon and label */
}

.brand {
    color: #c0395c;
}

/* Fill available space for nav-link */
.nav-link {
    display: flex;
    /* Keep everything aligned */
    align-items: center;
    width: 100%;
    padding: 10px 15px;
    /* Add padding for better hover area */
    border-radius: 10px;
    /* Rounded corners */
    color: #c0395c;
    /* Text color */
    text-decoration: none;
    /* Remove underline */
}

.nav-link:hover {
    background: rgba(255, 255, 255, 0.6);
    /* Lighter background on hover */
}

/* Icon */
.icon {
    width: 20px;
    height: 20px;
    color: #c0395c;
}
</style>