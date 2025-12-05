import { defineStore } from "pinia";

export const useSignUpStore = defineStore('signup-store', () => {
    const registerInput = {
        name: '',
        email: "",
        password: "",
        otpCode: ''
    };

    return { registerInput }
})