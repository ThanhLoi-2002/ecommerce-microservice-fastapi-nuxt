export type IResponse<T = any> = {
  // status: boolean;
  message: string;
  data?: T;
}

export enum SortEnum {
  ASC = "ASC",
  DESC = "DESC"
}

export enum GenderEnum {
  MALE = "MALE",
  FEMALE = "FEMALE",
  BOTH = "BOTH"
}

export enum RoleEnum {
  ADMIN = "ADMIN",
  USER = "USER"
}

export enum ConversationEnum {
  PRIVATE = "PRIVATE",
  GROUP = "GROUP"
}

export enum MessageTypeEnum {
  TEXT = "TEXT",
  IMAGE = "IMAGE",
  FILE = "FILE"
}

export type OptionType = {
  label: string
  value: string
}

export type PaginationType<T = any> = {
  items: T[]
  total: number
  page: number
  limit: number
  total_pages: number
  metadata: any
}

export type ImageType = {
  public_id: string
  url: string
}

export type PageginationFilter = {
  page: number
  limit: number
}

export type CategoryFilter = PageginationFilter & {
  name?: string
  sortBy?: string
  sortOrder?: SortEnum
  status?: boolean
  parent_only?: boolean
  is_metadata?: boolean
}

export interface Contact {
  id: number;
  name: string;
  phone?: string;
  avatar: string;
  section?: string;
  gender?: string;
  birthDate?: string;
  coverImage?: string;
}