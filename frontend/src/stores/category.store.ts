import type { PaginationType } from '@/types/common';
import type { CategoryType } from './../types/entities';
import { defineStore } from "pinia";

export const useCategoryStore = defineStore("category", {
    state: () => ({
        isLoading: false as boolean,
        categories: [] as CategoryType[],
        total_pages: 0,
        total: 0,
        metadata: {} as any
    }),

    actions: {
        setIsLoading(value: boolean) {
            this.isLoading = value
        },
        setCategories(data: PaginationType<CategoryType>) {
            this.categories = data.items
            this.total_pages = data.total_pages
            this.total = data.total
            this.metadata = data.metadata
        },
    }
});
