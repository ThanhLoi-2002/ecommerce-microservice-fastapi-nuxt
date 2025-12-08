import type { IResponse } from "@/types/common";
import axios from "./axios";
import type { SignUpFormType, SignInFormType } from "@/types/formType";

const signUp = async (data: SignUpFormType) => {
  return axios.post<IResponse>(`/auth/signup`, data);
};

const signIn = async (data: SignInFormType) => {
  return axios.post<IResponse<string>>("/auth/signin", data);
};

export const authApi = {
    signUp, signIn
}