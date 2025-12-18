import type { ImageType, RoleEnum, GenderEnum } from "./common";

export type BaseEntity = {
  id: number;
  created_at: string;
  updated_at: string;
};

export type UserType = BaseEntity & {
  email: string
  name: string
  role: RoleEnum
  avatar?: ImageType
}

export type CategoryType = BaseEntity & {
  name: string;
  slug: string;
  description: string | null
  img: ImageType;
  pid: number | null;
  gender: GenderEnum;
  status: boolean;
  children_count: number;
  parent?: CategoryType
}