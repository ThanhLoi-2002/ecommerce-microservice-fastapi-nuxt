import type { SizeType } from './../types/entities';
import { defineStore } from "pinia";

export const useSizeStore = defineStore("size", {
    state: () => ({
        isLoading: false as boolean,
        sizes: [] as SizeType[],
    }),

    actions: {
        setIsLoading(value: boolean) {
            this.isLoading = value
        },
        setSizes(data: SizeType[]) {
            this.sizes = data
        },
        add(size: SizeType) {
            this.sizes.push(size)
        },
        update(size: SizeType) {
            this.sizes = this.sizes.map(s => s.id == size.id ? size : s)
        },
        delete(id: number) {
            this.sizes = this.sizes.filter(s => s.id != id)
        }
    }
});
