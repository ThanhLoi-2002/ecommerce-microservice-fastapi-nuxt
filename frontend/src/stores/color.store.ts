import type { ColorType } from './../types/entities';
import { defineStore } from "pinia";

export const useColorStore = defineStore("color", {
    state: () => ({
        isLoading: false as boolean,
        colors: [] as ColorType[],
    }),

    actions: {
        setIsLoading(value: boolean) {
            this.isLoading = value
        },
        setList(data: ColorType[]) {
            this.colors = data
        },
        add(data: ColorType) {
            console.log(data)
            this.colors.push(data)
        },
        update(data: ColorType) {
            this.colors = this.colors.map(c => c.id == data.id ? data : c)
        },
        delete(id: number) {
            this.colors = this.colors.filter(c => c.id != id)
        }
    }
});
