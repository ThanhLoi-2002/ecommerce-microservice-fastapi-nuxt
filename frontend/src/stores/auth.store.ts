import { authApi } from "@/api/auth.api";
import { useToast } from "@/composables/useToast";
import type { SignInFormType, SignUpFormType } from "@/types/formType";
import { setRefreshToken, setToken } from "@/utils/token";
import { defineStore } from "pinia";
import { useUserStore } from "./user.store";
import router from '@/router';

const toast = useToast();
const userStore = useUserStore();

export const useAuthStore = defineStore("auth", {
  state: () => ({
    isLoading: false,
  }),

  actions: {
    async signInHandler(form: SignInFormType) {
      this.isLoading = true
      try {
        const { data }: any = await authApi.signIn(form);
        setToken(data.token)
        setRefreshToken(data.refreshToken)
        router.push('/')
        await userStore.getMeHandler()
      } catch (e: any) {
        toast.error(e.message)
      } finally {
        this.isLoading = false
      }
    },

    async signUpHandler(form: SignUpFormType) {
      this.isLoading = true
      try {
        const { message }: any = await authApi.signUp(form);
        toast.success(message)
        router.push('/signin')
      } catch (e: any) {
        toast.error(e.message)
      } finally {
        this.isLoading = false
      }
    }
  }
});
