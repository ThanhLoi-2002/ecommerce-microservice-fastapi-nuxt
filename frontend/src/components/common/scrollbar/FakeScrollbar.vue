<template>
    <div class="scroll-wrapper" @mouseenter="show = true" @mouseleave="show = false">
        <!-- Content -->
        <div ref="contentRef" class="scroll-content" @scroll="onScroll">
            <slot />
        </div>

        <!-- Fake scrollbar -->
        <div v-show="show" class="scrollbar-track">
            <div class="scrollbar-thumb" :style="thumbStyle" @mousedown="onMouseDown" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const contentRef = ref < HTMLDivElement | null > (null)
const show = ref(false)

const thumbHeight = ref(40)
const thumbTop = ref(0)

const updateThumb = () => {
    const el = contentRef.value
    if (!el) return

    const ratio = el.clientHeight / el.scrollHeight
    thumbHeight.value = Math.max(el.clientHeight * ratio, 30)
    thumbTop.value =
        (el.scrollTop / el.scrollHeight) * el.clientHeight
}

const onScroll = () => updateThumb()

const onMouseDown = (e: MouseEvent) => {
    const startY = e.clientY
    const startTop = thumbTop.value

    const onMove = (ev: MouseEvent) => {
        const el = contentRef.value
        if (!el) return

        const delta = ev.clientY - startY
        const maxTop = el.clientHeight - thumbHeight.value
        const newTop = Math.min(Math.max(startTop + delta, 0), maxTop)

        thumbTop.value = newTop
        el.scrollTop =
            (newTop / el.clientHeight) * el.scrollHeight
    }

    const onUp = () => {
        document.removeEventListener('mousemove', onMove)
        document.removeEventListener('mouseup', onUp)
    }

    document.addEventListener('mousemove', onMove)
    document.addEventListener('mouseup', onUp)
}

const thumbStyle = computed(() => ({
    height: `${thumbHeight.value}px`,
    transform: `translateY(${thumbTop.value}px)`
}))

onMounted(updateThumb)
</script>

<style>
.scroll-wrapper {
    position: relative;
    height: 100%;
    overflow: hidden;
}

/* Content */
.scroll-content {
    height: 100%;
    overflow-y: scroll;
    padding-right: 10px;

    /* Ẩn scrollbar native */
    scrollbar-width: none;
}

.scroll-content::-webkit-scrollbar {
    display: none;
}

/* Track */
.scrollbar-track {
    position: absolute;
    top: 4px;
    right: 2px;
    bottom: 4px;
    width: 4px;
}

/* Thumb */
.scrollbar-thumb {
    width: 100%;
    background: rgb(128, 180, 248);
    border-radius: 4px;
    cursor: pointer;
    transition: opacity 0.2s;
}
</style>