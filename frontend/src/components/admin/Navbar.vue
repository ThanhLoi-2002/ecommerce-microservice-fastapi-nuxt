<template>
    <nav class="navbar navbar-light bg-white shadow-sm px-4">
        <button class="btn btn-sm btn-light border" @click="$emit('toggle')">
            <i class="pi pi-bars" style="font-size: 1rem"></i>
        </button>

        <!-- <span class="navbar-brand mb-0 h5">Dashboard</span> -->

        <div class="d-flex align-items-center justify-content-center">
            <div class="icon-btn mr-3">
                <i class="pi pi-bell" style="font-size: 1.2rem"></i>
            </div>

            <img :src="user?.avatar?.url || DEFAULT_AVATAR" class="rounded-circle border" width="36" height="36"
                style="object-fit: cover" />
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