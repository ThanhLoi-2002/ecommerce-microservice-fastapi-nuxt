
import { userApi } from '@/api/user.api';
import { useUserStore } from '@/stores/user.store';
import type { UserProfileFormType } from '@/types/form/user.form';
import { reactive } from 'vue';
import { useToast } from './useToast';
import { useAuthStore } from '@/stores/auth.store';
import type { ImageType } from '@/types/entities';
import { useUpload } from './useUpload';
import mediaApi from '@/api/media.api';
import { storeToRefs } from 'pinia';

const userProfileFormValue: UserProfileFormType = {
    name: "",
    email: ""
}

export function useUser() {
    const userProfileForm = reactive<UserProfileFormType>(userProfileFormValue);
    const userStore = useUserStore();
    const authStore = useAuthStore();
    const toast = useToast()
    const { upload } = useUpload()

    const { user } = storeToRefs(userStore)

    const getMe = async () => {
        authStore.setIsAuthLoading(true)

        try {
            const { data }: any = await userApi.getMe()
            userStore.setUser(data)
            authStore.setIsAuth(true)
        }
        catch (error: any) {
            toast.error(error.message)
            authStore.setIsAuth(false)
        }
        finally {
            authStore.setIsAuthLoading(false)
        }
    }

    const updateProfile = async (userProfile: UserProfileFormType, callback: () => void) => {
        userStore.setIsLoading(true)

        try {
            const { data, message }: any = await userApi.updateProfile(userProfile)
            userStore.setUser(data)
            toast.success(message)
            callback()
        }
        catch (error: any) {
            toast.error(error.message)
        }
        finally {
            userStore.setIsLoading(false)
        }
    }

    const updateAvatar = async (file: File) => {
        const result: ImageType | null = await upload(file)

        if (result) {
            try {
                const { data, message }: any = await userApi.updateAvatar(result)
                await mediaApi.deleteFile(user.value?.avatar?.public_id!)
                userStore.setUser(data)
                toast.success(message)
            }
            catch (error: any) {
                toast.error(error.message)
            }
        }
    }

    return { userProfileForm, getMe, updateProfile, updateAvatar }
}