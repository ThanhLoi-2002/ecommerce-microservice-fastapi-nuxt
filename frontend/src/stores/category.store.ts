import type { GenderEnum, ImageType, PaginationType } from '@/types/common';
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

    getters: {
        categoriesByGender: (state) => {
            return (gender: GenderEnum) => state.categories.filter(c => c.gender === gender).sort((a, b) => a.name.localeCompare(b.name))
        }
    },

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
        setActiveCount(value: boolean) {
            this.metadata.activeCount += value ? 1 : -1
        },
        changeImage(id: number, img: ImageType) {
            this.categories = this.categories.map(c =>
                c.id === id ? { ...c, img } : c
            )
        }
    }
});
