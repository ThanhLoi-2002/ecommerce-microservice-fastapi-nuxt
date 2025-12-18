import type { CategoryFilter, IResponse, PaginationType } from "@/types/common";
import axios from "./axios";
import type { CategoryType } from "@/types/entities";
import type { CategoryFormType } from "@/types/form/category.form";

const getCategories = async (filters: CategoryFilter) => {
    const { page, ...query } = filters;

    let filterOptions = `page=${page ?? 1}`;

    for (const [key, value] of Object.entries(query)) {
        if (value != null || value != undefined)
            filterOptions += `&${key}=${Array.isArray(value) ? value.join(",") : value
                }`;
    }

    return await axios.get<IResponse<PaginationType<CategoryType>>>(`/categories?${filterOptions}`);
};

const getCategory = async (id: number) => {
    return await axios.get<IResponse<CategoryType>>(`/categories/${id}`);
}

const createOrUpdate = async (data: CategoryFormType, id?: number) => {
    if (id)
        return await axios.put<IResponse<CategoryType>>(`/categories/${id}`, data);
    else return await axios.post<IResponse<CategoryType>>(`/categories`, data);
}

const deleteCategory = async (id: number) => {
    return await axios.delete<IResponse<CategoryType>>(`/categories/${id}`);
}

export const categoryApi = {
    getCategories, getCategory, createOrUpdate, deleteCategory
}