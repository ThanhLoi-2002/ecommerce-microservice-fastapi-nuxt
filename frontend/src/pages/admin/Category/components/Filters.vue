<template>
    <div class="row mb-4">
        <div class="col-md-4">
            <input type="text" class="form-control" placeholder="🔍 Tìm kiếm danh mục..." v-model="filters.name"
                @input="debouncedSearch" />
        </div>
        <div class="col-md-3">
            <select class="form-control" v-model="filters.status" @change="setFilters('status', filters.status)">
                <option :value="undefined">Tất cả trạng thái</option>
                <option :value="true">Đang hoạt động</option>
                <option :value="false">Không hoạt động</option>
            </select>
        </div>
        <div class="col-md-2">
            <select class="form-control" v-model="filters.parentOnly"
                @change="setFilters('parentOnly', filters.parentOnly)">
                <option :value="undefined">Tất cả</option>
                <option :value="true">Danh mục cha</option>
            </select>
        </div>
        <div class="col-md-2">
            <select class="form-control" @change="handleSort($event)">
                <option value="">Sắp xếp</option>
                <option :value="`name:${SortEnum.ASC}`">Tên A → Z</option>
                <option :value="`name:${SortEnum.DESC}`">Tên Z → A</option>
            </select>
        </div>

        <div class="col-md-1">
            <button class="btn btn-outline-secondary btn-block" @click="resetFilters">
                🔄
            </button>
        </div>
    </div>
</template>
<script setup lang="ts">
import { useCategory } from '@/composables/useCategory';
import { SortEnum, type CategoryFilter } from '@/types/common';

const props = defineProps<{
    filters: CategoryFilter,
    setFilters: <K extends keyof CategoryFilter>(key: K,
        value: CategoryFilter[K]) => void
    resetFilters: () => void
}>()

const { getCategories } = useCategory()

let searchTimeout: any = null;
const debouncedSearch = () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        props.setFilters("page", 1);
        getCategories(props.filters)
    }, 500);
};

const handleSort = (e: Event) => {
    const value = (e.target as HTMLSelectElement).value
    if (!value) {
        props.setFilters('sortBy', undefined)
        props.setFilters('sortOrder', undefined)
        return
    }

    const [sortBy, sortOrder] = value.split(':')
    props.setFilters('sortBy', sortBy)
    props.setFilters('sortOrder', sortOrder as SortEnum)
}

</script>