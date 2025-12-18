import type { ImageType, IResponse } from "@/types/common";
import axios from "./axios";
import type { UserProfileFormType } from "@/types/form/user.form";

const getMe = async () => {
  return axios.get<IResponse>(`/users/me`,);
};

const updateProfile = async (data: UserProfileFormType) => {
  return axios.put<IResponse>(`/users`, data);
};

const updateAvatar = async (avatar: ImageType) => {
  return axios.put<IResponse>(`/users/update-avatar`, { ...avatar });
};

export const userApi = {
  getMe, updateProfile, updateAvatar
}