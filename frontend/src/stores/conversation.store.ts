import type { PaginationType } from '@/types/common';
import { defineStore } from "pinia";

export const useConversationStore = defineStore("conversation", {
    state: () => ({
        isLoading: false as boolean,
        conversations: [] as any[],
        selectedConversation: undefined as any,
        total_pages: 0,
        total: 0,
    }),

    actions: {
        setIsLoading(value: boolean) {
            this.isLoading = value
        },
        setConversations(data: PaginationType<any>) {
            this.conversations = data.items
            this.total_pages = data.total_pages
            this.total = data.total
        },
        setSelectedConversation(conversation: any){
            this.selectedConversation = conversation
        }
    }
});
