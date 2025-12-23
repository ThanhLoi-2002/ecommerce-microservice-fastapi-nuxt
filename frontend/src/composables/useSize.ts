
import { useToast } from './useToast';
import { sizeApi } from '@/api/size.api';
import { useSizeStore } from '@/stores/size.store';
import type { SizeFormType } from '@/types/form/size.form';
import { storeToRefs } from 'pinia';

export function useSize() {
    const toast = useToast()
    const sizeStore = useSizeStore()
    const { isLoading, sizes } = storeToRefs(sizeStore)

    const getSizes = async () => {
        if (sizes.value.length > 0) return
        try {
            sizeStore.setIsLoading(true)
            const { data }: any = await sizeApi.getList()
            sizeStore.setSizes(data)
        }
        catch (error: any) {
            toast.error(error.message)
        } finally {
            sizeStore.setIsLoading(false)
        }
    }

    const create = async (values: SizeFormType) => {
        try {
            const { message, data }: any = await sizeApi.create(values)
            toast.success(message)
            sizeStore.add(data)
            return true
        } catch (error: any) {
            toast.error(error.message)
            return false
        }
    }

    const update = async (id: number, values: SizeFormType) => {
        try {
            const { message, data }: any = await sizeApi.update(id, values)
            toast.success(message)
            sizeStore.update(data)
            return true
        } catch (error: any) {
            toast.error(error.message)
            return false
        }
    }

    const deleteSize = async (id: number) => {
        try {
            const { message }: any = await sizeApi.deleteSize(id)
            toast.success(message)
            sizeStore.delete(id)
            return true
        } catch (error: any) {
            toast.error(error.message)
            return false
        }
    }

    return { getSizes, deleteSize, create, update }
}