import { ref } from 'vue'

interface Toast {
  id: number
  message: string
  type: 'success' | 'error' | 'info' | 'warning'
}

const toasts = ref<Toast[]>([])

let id = 0

export function useToast() {
  const add = (message: string, type: 'success' | 'error' | 'info' | 'warning' = 'info', duration = 4000) => {
    const toastId = ++id
    toasts.value.push({ id: toastId, message, type })

    setTimeout(() => {
      remove(toastId)
    }, duration)
  }

  const remove = (id: number) => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }

  const success = (msg: string) => add(msg, 'success')
  const error = (msg: string) => add(msg, 'error')
  const info = (msg: string) => add(msg, 'info')
  const warning = (msg: string) => add(msg, 'warning')

  return { toasts, success, error, info, warning, remove }
}