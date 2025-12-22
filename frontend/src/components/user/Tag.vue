<template>
    <span class="tag">
        {{ label }}
    </span>
</template>
<script setup lang="ts">
const props = defineProps<{
    label: string
    onClick?: () => void
}>()
</script>
<style>
.tag {
    padding: 6px 12px;
    background: white;
    border: 1px solid rgb(77, 77, 77, 0.2);
    border-bottom-right-radius: 6px;
    border-top-left-radius: 6px;
    font-size: 0.85rem;
    cursor: pointer;
    transition: background 0.3s;
}

.tag:hover {
    border: 1px solid rgb(0, 0, 0, 0.3);
}
</style>