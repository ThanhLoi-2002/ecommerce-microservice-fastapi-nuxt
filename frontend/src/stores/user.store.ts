import { userApi } from '@/api/user.api';
import { type AvatarType, type UserType } from './../types/entities';
import { defineStore } from "pinia";
import { useToast } from '@/composables/useToast';
import { removeToken } from '@/utils/token';
import router from '@/router';
import type { UserProfileFormType } from '@/types/form/user.form';

const toast = useToast()

export const useUserStore = defineStore("user", {
    state: () => ({
        isAuth: false as boolean,
        user: null as UserType | null,
        isLoading: false as boolean,
    }),

    actions: {
        updateUser(user: UserType) {
            this.user = user
        },

        async getMeHandler() {
            this.isLoading = true

            try {
                const { data }: any = await userApi.getMe()
                this.user = data
                this.isAuth = true
            }
            catch (error: any) {
                toast.error(error.message)
                this.isAuth = false
            }
            finally {
                this.isLoading = false
            }
        },

        async updateProfile(userProfile: UserProfileFormType, callback: () => void) {
            this.isLoading = true

            try {
                const { data, message }: any = await userApi.updateProfile(userProfile)
                this.user = data
                toast.success(message)
                callback()
            }
            catch (error: any) {
                toast.error(error.message)
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
