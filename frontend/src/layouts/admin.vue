<template>
  <div id="layout" class="">
    <div class="d-flex">
      <Sidebar :collapsed="collapsed" @toggle="collapsed = !collapsed" />

      <div class="main flex-grow-1">
        <Navbar @toggle="collapsed = !collapsed" />

        <div class="content p-4">
          <router-view />
        </div>
      </div>
    </div>
    <ChatButton/>
  </div>
</template>

<script setup lang="ts">
import Sidebar from '@/components/admin/Sidebar.vue';
import Navbar from '@/components/admin/Navbar.vue'
import { ref } from 'vue'
import ChatButton from '@/components/common/chat/ChatButton.vue';

const collapsed = ref(false)
</script>

<style scoped>
#layout {
  background-color: #f7f7f7;
}

.main {
  width: 100%;
}

.content {
  min-height: 100vh;
}
</style>
