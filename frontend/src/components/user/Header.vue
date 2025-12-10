<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm py-3">
        <div class="container">
            <router-link class="navbar-brand font-weight-bold" to="/">Clothify</router-link>

            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarContent">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarContent">
                <ul class="navbar-nav mx-auto">
                    <li class="nav-item">
                        <router-link class="nav-link" to="/">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/products">Product</router-link>
                    </li>
                </ul>

                <!-- RIGHT SIDE -->
                <div class="d-flex align-items-center">
                    <!-- Đã login -->
                    <div class="dropdown" v-if="isAuth">
                        <a class="d-flex align-items-center dropdown-toggle" href="#" role="button" id="avatarDropdown"
                            data-toggle="dropdown">
                            <img :src="user?.avatar?.url || DEFAULT_AVATAR" alt="avatar"
                                class="rounded-circle border" style="width: 38px; height: 38px; object-fit: cover;" />
                        </a>

                        <div class="dropdown-menu dropdown-menu-right" aria-labelledby="avatarDropdown">
                            <router-link class="dropdown-item" to="/profile">Profile</router-link>

                            <router-link class="dropdown-item" to="#" @click="userStore.logout">
                                Logout
                            </router-link>
                        </div>
                    </div>

                    <!-- Nếu chưa login -->
                    <div v-else>
                        <button class="btn btn-outline-dark mr-2" @click="$router.push('/auth/signin')" :disabled="isLoading">
                            Login
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </nav>
</template>

<script setup lang="ts">
import { useUserStore } from "@/stores/user.store";
import { DEFAULT_AVATAR } from "@/utils/constants";
import { storeToRefs } from "pinia";

// Lấy state từ composable
const userStore = useUserStore();
const { user, isAuth, isLoading } = storeToRefs(userStore)
</script>
