
import { reactive } from 'vue';
import { useToast } from './useToast';
import { GenderEnum, type CategoryFilter } from '@/types/common';
import { useUpload } from './useUpload';
import type { CategoryFormType } from '@/types/form/category.form';
import { useCategoryStore } from '@/stores/category.store';
import { categoryApi } from '@/api/category.api';

const categoryFormDefaultValue: CategoryFormType = {
    name: "",
    description: "",
    img: undefined,
    pid: undefined,
    status: false,
    gender: GenderEnum.MALE
}

export function useCategory() {
    const categoryForm = reactive<CategoryFormType>(categoryFormDefaultValue);
    const categoryStore = useCategoryStore()

    const toast = useToast()
    const { upload } = useUpload()

    const getCategories = async (filter: CategoryFilter) => {
        categoryStore.setIsLoading(true)

        try {
            const { data }: any = await categoryApi.getCategories({ ...filter, is_metadata: true })
            categoryStore.setCategories(data)
        }
        catch (error: any) {
            toast.error(error.message)
        } finally {
            categoryStore.setIsLoading(false)
        }
    }

    const createOrUpdate = async (values: CategoryFormType, id?: number) => {
        try {
            let result: any

            if(!id) {
                result = await upload(values.img);
                values.img = result
            }

            const { data }: any = await categoryApi.createOrUpdate(values, id)
            console.log(data)
            return true
        } catch (error: any) {
            console.log(error)
            toast.error(error.message)
            return false
        }
    }

    const getParentCategories = async () => {
        try {
            const { data }: any = await categoryApi.getCategories({ parentOnly: true, page: 1, limit: 100 })
            return data.items
        } catch (error: any) {
            toast.error(error.message)
            return []
        }
    }

    const getCategory = async (id: number) => {
        try {
            const { data }: any = await categoryApi.getCategory(id)
            return data
        } catch (error: any) {
            toast.error(error.message)
            return undefined
        }
    }

    return { categoryForm, getCategories, createOrUpdate, getParentCategories, getCategory }
}