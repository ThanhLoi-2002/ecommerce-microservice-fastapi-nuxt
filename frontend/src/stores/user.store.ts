import { type UserType } from './../types/entities';
import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
    state: () => ({
        user: null as UserType | null,
        isLoading: false as boolean,
    }),

    actions: {
        setUser(user: UserType | null) {
            this.user = user
        },
        setIsLoading(value: boolean) {
            this.isLoading = value
        }
    }
});
