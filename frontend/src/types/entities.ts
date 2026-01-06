import type { ImageType, RoleEnum, GenderEnum, ConversationEnum, MessageTypeEnum } from "./common";

export type BaseEntity = {
  id: number;
  created_at?: string;
  updated_at?: string;
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
  children: CategoryType[]
}

export type SizeType = BaseEntity & {
  name: string
}

export type ColorType = BaseEntity & {
  name: string
  code: string
}

export type MessageType = BaseEntity & {
  conversation_id: number
  sender_id: number;
  sender: UserType;
  content?: string;
  type: MessageTypeEnum;
  file?: {
    name: string;
    size: string;
    url: string;
    public_id: string
  };
  linkPreview?: {
    url: string;
    title: string;
    description: string;
    image: string;
  };
}

export type ConversationType = BaseEntity & {
    name?: string;
    type: ConversationEnum;
    lastMessage: string;
    lastMessageTime: string;
    unreadCount: number;
    members?: string[];
}