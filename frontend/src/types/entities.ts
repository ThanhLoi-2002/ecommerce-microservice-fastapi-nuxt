export enum RoleEnum {
    ADMIN = "ADMIN",
    USER = "USER"
 }

export type BaseEntity = {
  id: number;
  createdAt: string;
};

export type AvatarType = {
  public_id: string
  url: string
}


export type UserType = BaseEntity & {
    email: string
    name: string
    role: RoleEnum
    avatar?: AvatarType
}