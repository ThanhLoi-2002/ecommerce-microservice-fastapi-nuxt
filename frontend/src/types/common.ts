export interface IResponse<T = any> {
  // status: boolean;
  message: string;
  data?: T;
}

export type ImageType = {
  public_id: string
  url: string
}