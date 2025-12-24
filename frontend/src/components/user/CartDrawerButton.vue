<template>
    <div class="position-relative rounded-circle border p-2 d-flex justify-content-sm-center align-items-center"
        style="height: 40px; width: 40px" @click="openDrawer" v-if="isAuth">
        <i class="pi pi-shopping-cart" style="font-size: 18px;" />
        <span class="cart-badge" v-if="cartCount > 0">{{ cartCount }}</span>
    </div>

    <!-- Overlay -->
    <transition name="fade">
        <div v-if="drawerOpen" class="drawer-overlay" @click="closeDrawer"></div>
    </transition>

    <!-- Drawer -->
    <transition name="slide-right">
        <div v-if="drawerOpen" class="cart-drawer">
            <!-- Header -->
            <div class="drawer-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Giỏ hàng <span class="badge badge-dark">3</span></h5>
                <button class="close" @click="closeDrawer">&times;</button>
            </div>

            <!-- Content -->
            <div class="drawer-body">
                <div v-for="(item, index) in cartItems" :key="index" class="cart-item d-flex mb-3">
                    <img :src="item.image" class="cart-img" />

                    <div class="ml-3 flex-grow-1">
                        <div class="font-weight-bold">{{ item.name }}</div>
                        <small class="text-muted d-flex justify-content-between">
                            <span>Màu: {{ item.color }}</span>
                            <span>Size: {{ item.size }}</span>
                        </small>

                        <div class="d-flex justify-content-between align-items-center mt-2">
                            <div class="quantity d-flex gap-1">
                                <button class="btn btn-outline-dark d-flex align-items-center justify-content-center"
                                    style="height: 25px; width: 25px;">-</button>
                                <div>{{ item.qty }}</div>
                                <button class="btn btn-outline-dark d-flex align-items-center justify-content-center"
                                    style="height: 25px; width: 25px;">+</button>
                            </div>
                            <div class="text-danger font-weight-bold">
                                {{ item.price }}đ
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Footer -->
            <div class="drawer-footer">
                <div class="d-flex justify-content-between mb-2">
                    <span>Tổng cộng</span>
                    <strong>3.736.000đ</strong>
                </div>
                <router-link class="btn btn-dark btn-block" to="/cart" @click="drawerOpen = false">XEM GIỎ HÀNG</router-link>
            </div>
        </div>
    </transition>
</template>
<script setup lang="ts">
import { useAuthStore } from '@/stores/auth.store';
import { storeToRefs } from 'pinia';
import { ref } from 'vue';

const authStore = useAuthStore();
const { isAuth } = storeToRefs(authStore);

const drawerOpen = ref(false);
const cartCount = ref(3);

const cartItems = ref([
    {
        name: 'Chân váy Ruby Tweed Midi',
        color: 'Tím đậm',
        size: 'S',
        qty: 1,
        price: '872.000',
        image: 'https://res.cloudinary.com/dqoepulwu/image/upload/v1766369533/fastapi/sj4wsajpbinpwdogu8r6.webp'
    },
    {
        name: 'Chân váy Ruby Tweed Midi',
        color: 'Tím đậm',
        size: 'XL',
        qty: 1,
        price: '872.000',
        image: 'https://res.cloudinary.com/dqoepulwu/image/upload/v1766369533/fastapi/sj4wsajpbinpwdogu8r6.webp'
    },
    {
        name: 'Áo Blazer Ruby Signature',
        color: 'Tím đậm',
        size: 'XXL',
        qty: 1,
        price: '1.992.000',
        image: 'https://res.cloudinary.com/dqoepulwu/image/upload/v1766369533/fastapi/sj4wsajpbinpwdogu8r6.webp'
    }
]);

const openDrawer = () => (drawerOpen.value = true);
const closeDrawer = () => (drawerOpen.value = false);
</script>
<style>
/* Badge giỏ hàng */
.cart-badge {
    position: absolute;
    top: -5px;
    right: -2px;
    background: #dc3545;
    color: #fff;
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 999px;
}

/* OVERLAY */
.drawer-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    z-index: 1040;
}

/* DRAWER */
.cart-drawer {
    position: fixed;
    top: 0;
    right: 0;
    width: 380px;
    height: 100vh;
    background: #fff;
    z-index: 1050;
    display: flex;
    flex-direction: column;
}

/* HEADER */
.drawer-header {
    padding: 16px;
    border-bottom: 1px solid #eee;
}

/* BODY */
.drawer-body {
    padding: 16px;
    overflow-y: auto;
    flex: 1;
}

/* FOOTER */
.drawer-footer {
    padding: 16px;
    border-top: 1px solid #eee;
}

/* CART ITEM */
.cart-img {
    width: 70px;
    height: auto;
    border-radius: 4px;
}

.quantity button {
    width: 26px;
    border: 1px solid #ddd;
    background: none;
}

/* ANIMATION */
.slide-right-enter-active,
.slide-right-leave-active {
    transition: transform 0.3s ease;
}

.slide-right-enter-from {
    transform: translateX(100%);
}

.slide-right-enter-to {
    transform: translateX(0);
}

.slide-right-leave-from {
    transform: translateX(0);
}

.slide-right-leave-to {
    transform: translateX(100%);
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>