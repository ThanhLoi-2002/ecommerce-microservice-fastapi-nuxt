<template>
    <nav class="navbar navbar-light bg-white shadow-sm px-4">
        <button class="btn btn-sm btn-light border" @click="$emit('toggle')">
            <i class="pi pi-bars" style="font-size: 1rem"></i>
        </button>

        <div class="d-flex align-items-center justify-content-center">
            <div class="icon-btn mr-3">
                <i class="pi pi-bell" style="font-size: 1.2rem"></i>
            </div>

            <div class="dropdown">
                <a class="d-flex align-items-center dropdown-toggle" href="#" role="button" id="avatarDropdown"
                    data-toggle="dropdown">
                    <img :src="user?.avatar?.url || DEFAULT_AVATAR" alt="avatar" class="rounded-circle border"
                        style="width: 38px; height: 38px; object-fit: cover;" />
                </a>

                <div class="dropdown-menu dropdown-menu-right" aria-labelledby="avatarDropdown">
                    <router-link class="dropdown-item" to="#" @click="userStore.logout">
                        Logout
                    </router-link>
                </div>
            </div>
        </div>
    </nav>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user.store';
import { DEFAULT_AVATAR } from '@/utils/constants';
import { storeToRefs } from 'pinia';

const userStore = useUserStore()
const { user } = storeToRefs(userStore)
</script>