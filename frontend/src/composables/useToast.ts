// src/composables/useToast.ts
import { ref } from "vue"

interface Toast {
  id: number
  message: string
  type: 'success' | 'error' | 'info' | 'warning'
}

const toasts = ref<Toast[]>([])
let id = 0

function add(message: string, type: Toast['type'] = 'info', duration = 4000) {
  const toastId = ++id
  toasts.value.push({ id: toastId, message, type })
  setTimeout(() => remove(toastId), duration)
}

function remove(id: number) {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

function success(msg: string) { add(msg, 'success') }
function error(msg: string) { add(msg, 'error') }
function info(msg: string) { add(msg, 'info') }
function warning(msg: string) { add(msg, 'warning') }

export function useToast() {
  return { toasts, success, error, info, warning, remove }
}
