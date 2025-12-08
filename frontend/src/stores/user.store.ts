import { userApi } from '@/api/user.api';
import { type UserType } from './../types/entities';
import { defineStore } from "pinia";
import { useToast } from '@/composables/useToast';
import { removeToken } from '@/utils/token';
import router from '@/router';

export const useUserStore = defineStore("user", {
    state: () => ({
        isAuth: false as boolean,
        user: null as UserType | null,
        isLoading: false as boolean,
    }),

    actions: {
        async getMeHandler() {
            const toast = useToast()
            this.isLoading = true

            try {
                const { data }: any = await userApi.getMe()
                this.user = data
                this.isAuth = true
            }
            catch (error: any) {
                toast.error(error.response?.data?.message || "Lỗi tải thông tin người dùng")
                this.isAuth = false
            }
            finally {
                this.isLoading = false
            }
        },

        logout() {
            removeToken()
            this.isAuth = false
            this.user = null
            router.push("/")
        }
    }
});
