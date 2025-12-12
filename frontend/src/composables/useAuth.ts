
import { useAuthStore } from '@/stores/auth.store';
import type { SignInFormType, SignUpFormType } from '@/types/form/auth.form';
import { reactive } from 'vue';
import { useToast } from './useToast';
import { removeToken, setRefreshToken, setToken } from '@/utils/token';
import router from '@/router';
import { authApi } from '@/api/auth.api';
import { useUser } from './useUser';
import { useUserStore } from '@/stores/user.store';
import { storeToRefs } from 'pinia';
import { RoleEnum } from '@/types/entities';

const signUpFormValue: SignUpFormType = {
    name: "",
    email: "",
    password: ""
}

const signInFormValue: SignInFormType = {
    email: "",
    password: ""
}

export function useAuth() {
    const signUpForm = reactive<SignUpFormType>(signUpFormValue);
    const signInForm = reactive<SignInFormType>(signInFormValue);
    const authStore = useAuthStore()
    const userStore = useUserStore()
    const { user } = storeToRefs(userStore)
    const { getMe } = useUser()
    const toast = useToast()

    const signIn = async (form: SignInFormType) => {
        authStore.setIsLoading(true)
        try {
            const { data }: any = await authApi.signIn(form);
            setToken(data.token)
            setRefreshToken(data.refreshToken)
            router.push('/')
            await getMe()
        } catch (e: any) {
            toast.error(e.message)
        } finally {
            authStore.setIsLoading(false)
        }
    }

    const signUp = async (form: SignUpFormType) => {
        authStore.setIsLoading(true)
        try {
            const { message }: any = await authApi.signUp(form);
            toast.success(message)
            router.push('/auth/signin')
        } catch (e: any) {
            toast.error(e.message)
        } finally {
            authStore.setIsLoading(false)
        }
    }

    const logout = () => {
        removeToken()
        if (user?.value?.role == RoleEnum.ADMIN) {
            router.push("/auth/signin")
        } else {
            router.push("/")
        }
        userStore.setUser(null)
        authStore.setIsAuth(false)
    }

    return { signUpForm, signInForm, signIn, signUp, logout }
}