// src/composables/useSocket.ts
import { inject } from "vue";
import { Socket } from "socket.io-client";
import { SOCKET_KEY } from "@/plugins/socketio";

export function useSocket(): Socket {
  const socket = inject<Socket>(SOCKET_KEY);
  if (!socket) {
    throw new Error("Socket.IO not provided");
  }
  return socket;
}
