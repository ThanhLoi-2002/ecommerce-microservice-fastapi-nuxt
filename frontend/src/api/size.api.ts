import type { IResponse } from "@/types/common";
import axios from "./axios";
import type { SizeFormType } from "@/types/form/size.form";

const getList = async () => {
    return axios.get<IResponse>(`/sizes`,);
};

const update = async (id: number, data: SizeFormType) => {
    return axios.put<IResponse>(`/sizes/${id}`, data);
};

const create = async (data: SizeFormType) => {
    return axios.post<IResponse>(`/sizes`, data);
};

const deleteSize = async (id: number) => {
    return axios.delete<IResponse>(`/sizes/${id}`);
};

export const sizeApi = {
    create, update, getList, deleteSize
}