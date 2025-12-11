<template>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container-fluid">
            <span class="navbar-brand mb-0 h1">
                🛍️ Fashion Admin - {{ props.label }}
            </span>
        </div>
    </nav>
</template>
<script setup lang="ts">
const props = defineProps<{
  label: string;
}>();
</script>