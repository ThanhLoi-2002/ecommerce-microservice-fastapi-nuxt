<template>
    <div class="d-flex justify-content-between align-items-center mt-3">
        <div class="d-flex align-items-center">
            <span class="text-muted mr-2">
                Hiển thị {{ (page - 1) * limit + 1 }} -
                {{ Math.min(page * limit, total) }} /
                <strong>{{ total }}</strong> danh mục
            </span>
            <div class="">
                <select class="form-control" :value="limit" @change="changeLimit">
                    <option :value="1">1</option>
                    <option :value="5">5</option>
                    <option :value="10">10</option>
                    <option :value="20">20</option>
                    <option :value="50">50</option>
                </select>
            </div>
        </div>
        <nav>
            <ul class="pagination mb-0">
                <li class="page-item" :class="{ disabled: page === 1 }">
                    <a class="page-link" href="#" @click.prevent="changePage(page - 1)">‹</a>
                </li>
                <li v-for="p in displayPages" :key="p" class="page-item" :class="{ active: p === page }">
                    <a class="page-link" href="#">{{ p }}</a>
                </li>
                <li class="page-item" :class="{ disabled: page === total_pages }">
                    <a class="page-link" href="#" @click.prevent="changePage(page + 1)">›</a>
                </li>
            </ul>
        </nav>
    </div>
</template>
<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
    page: number
    limit: number
    total: number
    total_pages: number
    changeLimit: (e: any) => void
    changePage: (page: number) => void
}>()

const displayPages = computed(() => {
    const pages: number[] = [];
    const current = props.page;

    if (props.total_pages <= 7) {
        for (let i = 1; i <= props.total_pages; i++) {
            pages.push(i);
        }
    } else {
        pages.push(1);
        if (current > 3) pages.push(-1); // ellipsis

        for (let i = Math.max(2, current - 1); i <= Math.min(props.total_pages - 1, current + 1); i++) {
            pages.push(i);
        }

        if (current < props.total_pages - 2) pages.push(-1);
        pages.push(props.total_pages);
    }

    return pages;
});
</script>
<style></style>