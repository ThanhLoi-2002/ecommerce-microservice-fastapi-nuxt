<template>
    <div v-if="totalPages > 1" class="pagination-wrapper">
        <ul class="pagination-custom">
            <li :class="['page-item-custom', { disabled: currentPage === 1 }]" @click="changePage(currentPage - 1)">
                ‹
            </li>

            <li v-for="page in visiblePages" :key="page" :class="['page-item-custom', { active: currentPage === page }]"
                @click="changePage(page)">
                {{ page }}
            </li>

            <li :class="['page-item-custom', { disabled: currentPage === totalPages }]"
                @click="changePage(currentPage + 1)">
                ›
            </li>
        </ul>
    </div>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue'

const currentPage = ref<number>(1)
const visiblePages = computed<number[]>(() => {
    const pages: number[] = []
    const maxVisible = 5

    if (totalPages.value <= maxVisible) {
        for (let i = 1; i <= totalPages.value; i++) {
            pages.push(i)
        }
    } else if (currentPage.value <= 3) {
        for (let i = 1; i <= maxVisible; i++) {
            pages.push(i)
        }
    } else if (currentPage.value >= totalPages.value - 2) {
        for (let i = totalPages.value - maxVisible + 1; i <= totalPages.value; i++) {
            pages.push(i)
        }
    } else {
        for (let i = currentPage.value - 2; i <= currentPage.value + 2; i++) {
            pages.push(i)
        }
    }

    return pages
})

const totalPages = ref(2)

const changePage = (page: number): void => {
    if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
        window.scrollTo({ top: 0, behavior: 'smooth' })
    }
}
</script>
<style>
.pagination-wrapper {
    display: flex;
    justify-content: center;
    margin-top: 40px;
}

.pagination-custom {
    display: flex;
    gap: 5px;
    list-style: none;
    padding: 0;
    margin: 0;
}

.page-item-custom {
    cursor: pointer;
    padding: 8px 12px;
    border: 1px solid #ddd;
    background: white;
    color: #333;
    border-radius: 4px;
    transition: all 0.3s;
    font-size: 14px;
    user-select: none;
}

.page-item-custom:hover:not(.disabled):not(.active) {
    background: #f5f5f5;
}

.page-item-custom.active {
    background: #000;
    color: white;
    border-color: #000;
}

.page-item-custom.disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
</style>