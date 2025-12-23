import { GenderEnum, type CategoryFilter, type OptionType, type PaginationType } from "@/types/common";

export const ACCESS_TOKEN = "access_token";
export const REFRESH_TOKEN = "refresh_token";

export const DEFAULT_AVATAR = 'https://i.pravatar.cc/150?img=12'

export const genderOptions: OptionType[] = [
    { value: GenderEnum.MALE, label: 'Nam' },
    { value: GenderEnum.FEMALE, label: 'Nữ' },
    { value: GenderEnum.BOTH, label: 'Cả hai' },
]

export const paginationDefault: PaginationType = {
    items: [],
    total: 0,
    page: 0,
    limit: 0,
    total_pages: 0,
    metadata: {}
}

export const categoryFilterDefault: CategoryFilter = {
    page: 1,
    name: "",
    limit: 10,
    parent_only: undefined,
    sortBy: undefined,
    sortOrder: undefined,
    status: undefined,
    is_metadata: false
}

export const PRICE_MIN = 0
export const PRICE_MAX = 50000000
export const productFilterDefault = {
    sizes: [],
    colors: [],
    price: [PRICE_MIN, PRICE_MAX],
    discount: '',
    page: 1
}