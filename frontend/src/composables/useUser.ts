
import type { UserProfileFormType } from '@/types/form/user.form';
import { reactive } from 'vue';

const userProfileFormValue: UserProfileFormType = {
    name: "",
    email: ""
}

export function useUser() {
    const userProfileForm = reactive<UserProfileFormType>(userProfileFormValue);

    return { userProfileForm }
}