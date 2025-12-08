import {
    getRefreshToken,
    getToken,
    setToken,
    removeToken
} from "@/utils/token";
import axiosClient from "axios";
import axios from "axios";

const instance = axiosClient.create({
    baseURL: import.meta.env.VITE_API_URL + '/api/v1',
    withCredentials: false,
});

// --- FLAG tránh lặp vô hạn ---
let isRefreshing = false;
let queue: any[] = []; // để đợi refresh xong retry

// Add a request interceptor
instance.interceptors.request.use(
    async function (config: any) {
        let accessToken = getToken();

        if (accessToken) {
            config.headers["Authorization"] = accessToken
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
    async function (error) {
        // Any status codes that falls outside the range of 2xx cause this function to trigger
        // Do something with response error
        const originalRequest = error.config;
        if (error.status == 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            // ------- Nếu đang refresh, đợi -------
            if (isRefreshing) {
                return new Promise((resolve) => {
                    queue.push((token: string) => {
                        originalRequest.headers.Authorization = `Bearer ${token}`;
                        resolve(instance(originalRequest));
                    });
                });
            }
            isRefreshing = true;

            let refresh_token = getRefreshToken();

            try {
                const res = await axios.post(import.meta.env.VITE_API_URL + '/api/v1/auth/refresh-token', {
                    refreshToken: refresh_token,
                });

                const newToken = res.data.data.token;
                setToken(newToken);

                // Update Authorization cho request đầu
                originalRequest.headers.Authorization = `Bearer ${newToken}`;

                // Xử lý các request đang chờ
                queue.forEach((cb) => cb(newToken));
                queue = [];
                isRefreshing = false;

                return instance(originalRequest);

            } catch (err) {
                isRefreshing = false;
                queue = [];
                removeToken()
                window.location.href = '/'
                return Promise.reject(err);
            }
        }

        if (error?.response?.data) {
            return Promise.reject(error.response.data);
        }

        return Promise.reject(error);
    }
);

export default instance;
