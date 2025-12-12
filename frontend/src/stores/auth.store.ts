import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    isLoading: false,
    isAuth: false,
    isAuthLoading: false
  }),

  actions: {
    setIsLoading(value: boolean) {
      this.isLoading = value
    },
    setIsAuth(value: boolean) {
      this.isAuth = value
    },
    setIsAuthLoading(value: boolean) {
      this.isAuthLoading = value
    }
  }
});
