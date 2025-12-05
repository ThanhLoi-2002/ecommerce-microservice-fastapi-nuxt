// import { store } from "@/redux";
// import { authActions } from "@/redux/slice/authSlice";
// import { userActions } from "@/redux/slice/userSlice";
// import {
//   getRefreshToken,
//   getToken,
//   isTokenExpired,
//   setToken,
// } from "@/utils/token";
import axiosClient from "axios";
import axios from "axios";
import type { IResponse } from "../types/common";

const instance = axiosClient.create({
    baseURL: import.meta.env.VITE_API_URL,
    withCredentials: false,
});

// Add a request interceptor
instance.interceptors.request.use(
    async function (config: any) {
        // let accessToken = "" //getToken();
        // let refresh_token = getRefreshToken();
        // Do something before request is sent
        // if (accessToken && isTokenExpired(accessToken)) {
        //   try {
        //     const axiosClient = axios.create({
        //       baseURL: import.meta.env.VITE_API_URL,
        //       withCredentials: false,
        //     });
        //     const response = await axiosClient.get<IResponse>(
        //       "/auth/refresh-token",
        //       {
        //         headers: {
        //           Refresh_token: refresh_token,
        //         },
        //       }
        //     );

        //     if (response.data.status) {
        //       accessToken = response.data?.data.access_token;
        //       setToken(accessToken!);
        //     } else {
        //       store.dispatch(authActions.logout());
        //       store.dispatch(userActions.logout());
        //     }
        //   } catch (error) {
        //     return Promise.reject(error);
        //   }
        // }

        // config.headers.Authorization = "Bearer " + accessToken;

        // if (!config.headers.Accept && config.headers["Content-Type"]) {
        //   config.headers.Accept = "application/json";
        //   config.headers["Content-Type"] = "application/json; charset=utf-8";
        // }

        const token = localStorage.getItem("token")
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }

        return config;
    },
    function (error) {
        // Do something with request error
        return Promise.reject(error);
    }
);

// Add a response interceptor
instance.interceptors.response.use(
    function (response: any) {
        // Any status code that lie within the range of 2xx cause this function to trigger
        // Do something with response data
        return response.data;
    },
    function (error) {
        // Any status codes that falls outside the range of 2xx cause this function to trigger
        // Do something with response error
        if (error?.response?.data) {
            return Promise.reject(error.response.data);
        }

        return Promise.reject(error);
    }
);

export default instance;
