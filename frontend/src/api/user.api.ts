import type { IResponse } from "@/types/common";
import axios from "./axios";

const getMe = async () => {
  return axios.get<IResponse>(`/user/me`, );
};

export const userApi = {
    getMe
}