import type { IResponse } from "@/types/common";
import axios from "./axios";
import type { ColorFormType } from "@/types/form/color.form";

const getList = async () => {
    return axios.get<IResponse>(`/colors`,);
};

const update = async (id: number, data: ColorFormType) => {
    return axios.put<IResponse>(`/colors/${id}`, data);
};

const create = async (data: ColorFormType) => {
    return axios.post<IResponse>(`/colors`, data);
};

const deleteColor = async (id: number) => {
    return axios.delete<IResponse>(`/colors/${id}`);
};

export const colorApi = {
    create, update, getList, deleteColor
}