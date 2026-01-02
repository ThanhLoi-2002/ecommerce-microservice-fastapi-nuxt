<template>
    <div class="d-flex h-100">
        <!-- Left Sidebar - Conversations List -->
        <Conversations />

        <!-- Right Side - Chat Area -->
         <MessageContainer/>
        
    </div>
</template>

<script setup lang="ts">
import Conversations from './components/Conversations.vue';
import MessageContainer from './components/MessageContainer.vue';
</script>