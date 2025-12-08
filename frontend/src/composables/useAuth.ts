import type { SignInFormType, SignUpFormType } from '@/types/formType'
import { reactive } from 'vue';

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

    return { signUpForm, signInForm }
}