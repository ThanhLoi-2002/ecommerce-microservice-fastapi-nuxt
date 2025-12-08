import type { IResponse } from "@/types/common";
import axios from "./axios";


const headers = {
  "Content-Type": "multipart/form-data",
};

const uploadFile = (file: File) => {
  return axios.post<IResponse<any>>(`/media/upload`, { file }, { headers });
};

const uploadFiles = (files: FileList) => {
  const formData = new FormData();

  Array.from(files).forEach((file) => {
    formData.append("files", file);
  });

  return axios.post<IResponse<any>>(`/media/upload/multiple`, formData, { headers });
};

const deleteFile = (publiId: string) => {
  return axios.delete<IResponse<any>>(`/media/delete/${publiId}`,);
};

const mediaApi = {
  uploadFile,
  uploadFiles,
  deleteFile,
};

export default mediaApi;
