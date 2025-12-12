import mediaApi from "@/api/media.api"
import { useToast } from "./useToast"
import type { ImageType } from "@/types/entities"

export function useUpload() {
    const toast = useToast()

    async function upload(file: File): Promise<ImageType | null> {
        try {
            const { data }: any = await mediaApi.uploadFile(file)
            return {
                public_id: data.public_id,
                url: data.url
            }
        } catch (e: any) {
            toast.error(e.message)
            return null
        }
    }

    return {
        upload
    }
}