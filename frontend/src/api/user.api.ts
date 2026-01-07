import type { ImageType, IResponse, UserFilter } from "@/types/common";
import axios from "./axios";
import type { UserProfileFormType } from "@/types/form/user.form";

const getMe = async () => {
  return axios.get<IResponse>(`/users/me`,);
};

const searchUsers = async (filters: UserFilter) => {
  const { page, ...query } = filters;

    let filterOptions = `page=${page ?? 1}`;

    for (const [key, value] of Object.entries(query)) {
        if (value != null || value != undefined)
            filterOptions += `&${key}=${Array.isArray(value) ? value.join(",") : value
                }`;
    }
  return axios.get<IResponse>(`/users/search-users?${filterOptions}`,);
};

const updateProfile = async (data: UserProfileFormType) => {
  return axios.put<IResponse>(`/users`, data);
};

const updateAvatar = async (avatar: ImageType) => {
  return axios.put<IResponse>(`/users/update-avatar`, { ...avatar });
};

export const userApi = {
  getMe, updateProfile, updateAvatar, searchUsers
}