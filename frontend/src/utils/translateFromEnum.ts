import { GenderEnum } from "@/types/common";

export const categoryGender = (value?: GenderEnum) => {
    switch (value) {
        case GenderEnum.MALE: return 'Nam'
        case GenderEnum.FEMALE: return 'Nữ'
        default: return ''
    }
}