import type { GenderEnum } from "../common";

export type CategoryFormType = {
    name: string;
    description: string
    img?: any;
    pid?: number | null;
    status?: boolean;
    gender: GenderEnum
}