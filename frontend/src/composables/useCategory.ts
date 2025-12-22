
import { useToast } from './useToast';
import { type CategoryFilter } from '@/types/common';
import { useUpload } from './useUpload';
import type { CategoryFormType } from '@/types/form/category.form';
import { useCategoryStore } from '@/stores/category.store';
import { categoryApi } from '@/api/category.api';
import mediaApi from '@/api/media.api';

export function useCategory() {
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

            if (!id) {
                result = await upload(values.img);
                values.img = result
            }

            const { message }: any = await categoryApi.createOrUpdate(values, id)
            toast.success(message)
            return true
        } catch (error: any) {
            toast.error(error.message)
            return false
        }
    }

    const getParentCategories = async () => {
        try {
            const { data }: any = await categoryApi.getCategories({ parent_only: true, page: 1, limit: 100 })
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

    const deleteCategory = async (id: number) => {
        try {
            const { message }: any = await categoryApi.deleteCategory(id)
            toast.success(message)
            return true
        } catch (error: any) {
            toast.error(error.message)
            return false
        }
    }

    const changeStatus = async (id: number, status: boolean) => {
        try {
            const { message }: any = await categoryApi.changeStatus(id, status)
            toast.success(message)
            categoryStore.setActiveCount(status)
        } catch (error: any) {
            toast.error(error.message)
        }
    }

    const changeImage = async (id: number, file: File, public_id: string) => {
        try {
            const result = await upload(file);

            if (result) {
                const { message, data }: any = await categoryApi.changeImage(id, result)
                toast.success(message)
                mediaApi.deleteFile(public_id)
                categoryStore.changeImage(id, result)
                return data
            }
        } catch (error: any) {
            toast.error(error.message)
            return null
        }
    }

    return { getCategories, createOrUpdate, getParentCategories, getCategory, deleteCategory, changeStatus, changeImage }
}