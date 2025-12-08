
import type { SignInFormType, SignUpFormType } from '@/types/form/auth.form';
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