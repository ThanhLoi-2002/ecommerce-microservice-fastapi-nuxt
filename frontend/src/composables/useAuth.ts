// composables/useAuth.ts
// import { useAuthStore } from '@/stores/auth'
import { authApi } from '../api/auth.api';
import type { SignInFormType, SignUpFormType } from '@/types/formType'
import { storeToRefs } from 'pinia'
import { reactive } from 'vue';
import { useToast } from './useToast';

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
    const toast = useToast()
    //   const store = useAuthStore()
    //   const { user, isLoggedIn } = storeToRefs(store)

    const signUpForm = reactive<SignUpFormType>(signUpFormValue);
    const signInForm = reactive<SignInFormType>(signInFormValue);

    const signInHandler = async (form: SignInFormType) => {
        try {
            const { status, message, data }: any = await authApi.signIn(form);
            console.log(data)
        } catch (e: any) {
            toast.error(e.response?.data?.message)
        }
    }

    const logoutHandler = () => {

    }

    const signUpHandler = async (form: SignUpFormType) => {
        try {
            const { status, message, data }: any = await authApi.signUp(form);
            console.log(data)
        } catch (e: any) {
            toast.error(e.message)
        }
    }

    return { signInHandler, logoutHandler, signUpHandler, signUpForm, signInForm }
}