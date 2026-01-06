<template>
    <div v-if="isOpen && profile" class="modal d-block" style="background-color: rgba(0,0,0,0.5);">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header border-0 p-0">
                    <!-- Cover Image -->
                    <div class="position-relative w-100"
                        style="height: 200px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                        <div class="position-absolute" style="top: 16px; left: 16px;">
                            <button type="button" class="btn btn-light rounded-circle p-2" @click="close"
                                style="width: 40px; height: 40px;">
                                <i class="pi pi-arrow-left"></i>
                            </button>
                        </div>
                        <div class="position-absolute" style="top: 16px; right: 16px;">
                            <button type="button" class="btn btn-light rounded-circle p-2" @click="close"
                                style="width: 40px; height: 40px;">
                                <span>&times;</span>
                            </button>
                        </div>
                        <!-- Profile Avatar -->
                        <div class="position-absolute" style="bottom: -50px; left: 50%; transform: translateX(-50%);">
                            <div class="rounded-circle bg-white d-flex align-items-center justify-content-center border border-white"
                                style="width: 100px; height: 100px; border-width: 4px !important;">
                                <span style="font-size: 48px;">{{ profile.avatar }}</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-body pt-5 mt-4">
                    <!-- Name and Edit Icon -->
                    <div class="text-center mb-3">
                        <h5 class="font-weight-bold mb-0">
                            {{ profile.name }}
                            <i class="pi pi-pencil text-muted ml-2" style="font-size: 14px; cursor: pointer;"></i>
                        </h5>
                    </div>

                    <!-- Action Buttons -->
                    <div class="d-flex justify-content-center mb-4" style="gap: 8px;">
                        <button class="btn btn-light flex-fill">Kết bạn</button>
                        <button class="btn btn-primary flex-fill">Nhắn tin</button>
                    </div>

                    <!-- Personal Information -->
                    <div class="mb-3">
                        <h6 class="font-weight-bold mb-3">Thông tin cá nhân</h6>
                        <div class="d-flex justify-content-between py-2">
                            <span class="text-muted">Giới tính</span>
                            <span class="font-weight-bold">{{ profile.gender }}</span>
                        </div>
                        <div class="d-flex justify-content-between py-2">
                            <span class="text-muted">Ngày sinh</span>
                            <span class="font-weight-bold">{{ profile.birthDate }}</span>
                        </div>
                    </div>

                    <!-- Additional Options -->
                    <div class="border-top pt-3">
                        <div class="d-flex align-items-center py-2 hover-bg-light rounded px-2"
                            style="cursor: pointer;">
                            <i class="pi pi-users text-muted"></i>
                            <span class="ml-3 text-muted">Nhóm chung (0)</span>
                        </div>
                        <div class="d-flex align-items-center py-2 hover-bg-light rounded px-2"
                            style="cursor: pointer;">
                            <i class="pi pi-star text-muted"></i>
                            <span class="ml-3 text-muted">Chia sẻ danh thiếp</span>
                        </div>
                        <div class="d-flex align-items-center py-2 hover-bg-light rounded px-2"
                            style="cursor: pointer;">
                            <i class="pi pi-ban text-muted"></i>
                            <span class="ml-3 text-muted">Chặn tin nhắn và cuộc gọi</span>
                        </div>
                        <div class="d-flex align-items-center py-2 hover-bg-light rounded px-2"
                            style="cursor: pointer;">
                            <i class="pi pi-exclamation-triangle text-muted"></i>
                            <span class="ml-3 text-muted">Báo xấu</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import type { Contact } from '@/types/common';


const props = defineProps<{
    isOpen: boolean,
    profile?: Contact
    close: () => void
}>()
</script>
