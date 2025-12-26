<template>
  <div class="d-flex flex-column min-vh-100">
    <Header />
    <main class="flex-grow-1">
      <slot />
    </main>
    <ChatButton/>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import Header from '../components/user/Header.vue'
import Footer from '../components/user/Footer.vue'
import ChatButton from '@/components/common/chat/ChatButton.vue';
</script>
