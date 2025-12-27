// src/plugins/socket.ts
import { type App, inject } from "vue";
import { io, Socket } from "socket.io-client";

export const SOCKET_KEY = Symbol("socket");

export function createSocket(): Socket {
  const socket = io(import.meta.env.VITE_API_URL + '/', {
    transports: ["websocket"],
    autoConnect: false,
  });

  return socket;
}

export default {
  install(app: App, socket: Socket) {
    app.provide(SOCKET_KEY, socket);
    app.config.globalProperties.$socket = socket;
  },
};