<template>
  <div class="d-flex h-100">
    <Sidebar/>
    <main class="flex-grow-1">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import Sidebar from '@/components/chat/Sidebar.vue';

</script>
