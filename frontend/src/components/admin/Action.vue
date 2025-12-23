<template>
    <div class="card-header bg-white">
        <div class="d-flex justify-content-between align-items-center">
            <h5 class="mb-0"></h5>
            <button class="btn btn-primary" @click="props.onClick">
                ➕ {{ props.label }}
            </button>
        </div>
    </div>
</template>
<script setup lang="ts">
const props = defineProps<{
    onClick: () => void;
    label: string
}>();
</script>
<style></style>