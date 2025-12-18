<template>
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="alert alert-primary mb-0">
                <h4 class="mb-0">{{ total || 0 }}</h4>
                <small>Tổng danh mục</small>
            </div>
        </div>
        <div class="col-md-3">
            <div class="alert alert-success mb-0">
                <h4 class="mb-0">{{ activeCount || 0}}</h4>
                <small>Đang hoạt động</small>
            </div>
        </div>
        <div class="col-md-3">
            <div class="alert alert-info mb-0">
                <h4 class="mb-0">{{ parentCount || 0}}</h4>
                <small>Danh mục cha</small>
            </div>
        </div>
        <div class="col-md-3">
            <div class="alert alert-warning mb-0">
                <h4 class="mb-0">{{ childrenCount || 0}}</h4>
                <small>Danh mục con</small>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
defineProps<{
    childrenCount: number
    parentCount: number
    activeCount: number
    total: number
}>()
</script>
<style></style>