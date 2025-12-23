import { useColorStore } from '@/stores/color.store';
import { useToast } from './useToast';
import { storeToRefs } from 'pinia';
import { colorApi } from '@/api/color.api';
import type { ColorFormType } from '@/types/form/color.form';

export function useColor() {
    const toast = useToast()
    const colorStore = useColorStore()
    const { colors } = storeToRefs(colorStore)

    const getColors = async () => {
        if (colors.value.length > 0) return
        try {
            colorStore.setIsLoading(true)
            const { data }: any = await colorApi.getList()
            colorStore.setList(data)
        }
        catch (error: any) {
            toast.error(error.message)
        } finally {
            colorStore.setIsLoading(false)
        }
    }

    const create = async (values: ColorFormType) => {
        try {
            const { message, data }: any = await colorApi.create(values)
            toast.success(message)
            colorStore.add(data)
            return true
        } catch (error: any) {
            toast.error(error.message)
            return false
        }
    }

    const update = async (id: number, values: ColorFormType) => {
        try {
            const { message, data }: any = await colorApi.update(id, values)
            toast.success(message)
            colorStore.update(data)
            return true
        } catch (error: any) {
            toast.error(error.message)
            return false
        }
    }

    const deleteColor = async (id: number) => {
        try {
            const { message }: any = await colorApi.deleteColor(id)
            toast.success(message)
            colorStore.delete(id)
            return true
        } catch (error: any) {
            toast.error(error.message)
            return false
        }
    }

    return { getColors, deleteColor, create, update }
}