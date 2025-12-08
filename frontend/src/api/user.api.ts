import type { IResponse } from "@/types/common";
import axios from "./axios";
import type { UserProfileFormType } from "@/types/form/user.form";
import type { AvatarType } from "@/types/entities";

const getMe = async () => {
  return axios.get<IResponse>(`/user/me`,);
};

const updateProfile = async (data: UserProfileFormType) => {
  return axios.put<IResponse>(`/user`, data);
};

const updateAvatar = async (avatar: AvatarType) => {
  return axios.put<IResponse>(`/user/update-avatar`, { ...avatar });
};

export const userApi = {
  getMe, updateProfile, updateAvatar
}