<template>
    <div class="left-menu bg-primary d-flex flex-column align-items-center py-3">
        <!-- User Avatar -->
        <div class="menu-avatar mb-4">
            <img :src="user?.avatar?.url ?? DEFAULT_AVATAR" alt="User" class="rounded-circle">
        </div>

        <!-- Menu Items -->
        <div class="menu-items flex-grow-1 d-flex flex-column align-items-center">
            <router-link v-for="item in topMenu" :to="item.url" :key="item.title" class="menu-btn mb-3"
                :class="isActive(item.url)" :title="item.title">
                <i :class="`pi pi-${item.icon}`"></i>
            </router-link>
        </div>

        <!-- Bottom Menu Items -->
        <div class="menu-items-bottom d-flex flex-column align-items-center">
            <button class="menu-btn mb-3" title="Cài đặt">
                <i class="pi pi-cog"></i>
            </button>
        </div>
    </div>
</template>
<script setup lang="ts">
import { useUserStore } from '@/stores/user.store';
import { DEFAULT_AVATAR } from '@/utils/constants';
import { storeToRefs } from 'pinia';
import { useRoute } from 'vue-router';

const userStore = useUserStore()
const { user } = storeToRefs(userStore)
const route = useRoute()

const topMenu = [
    { title: 'Tin nhắn', icon: 'comment', url: '/chats/conversations' },
    { title: 'Shop', icon: 'shop', url: '/' },
]

const isActive = (path: string) => {
    if (path === '/') {
        return route.path === '/' ? 'active' : ''
    }
    return route.path.startsWith(path) ? 'active' : ''
}

</script>
<style>
/* Left Menu Bar */
.left-menu {
    width: 56px;
    background: linear-gradient(180deg, #0068ff 0%, #0052cc 100%);
    flex-shrink: 0;
}

.menu-avatar img {
    width: 40px;
    height: 40px;
    cursor: pointer;
}

.menu-btn {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    border: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.7);
    font-size: 18px;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.menu-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    color: white;
}

.menu-btn.active {
    background: rgba(255, 255, 255, 0.2);
    color: white;
}
</style>