<template>
    <div v-show="open" class="modal-backdrop" @click="closeModal" style="background-color: rgba(0,0,0,0.5);">
        <div class="modal-dialog modal-dialog-centered" @click.stop>
            <div class="modal-content">
                <div class="modal-header border-0">
                    <h5 class="modal-title font-weight-bold">
                        {{ title }}
                    </h5>
                    <button type="button" class="close" @click="closeModal">
                        <span>&times;</span>
                    </button>
                </div>
                <div class="modal-body p-4">
                    <slot />
                </div>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">

defineProps<{
    closeModal: () => void
    title: string
    open: boolean
}>()
</script>
<style>
.modal-backdrop {
    position: fixed;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
}

.modal-dialog {
    border-radius: 8px;
    max-width: 600px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
}
</style>