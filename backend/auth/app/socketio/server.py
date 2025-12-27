import json
import socketio
from app.socketio.presence import add_user_online, remove_user_online, get_online_users

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    client_manager=socketio.AsyncRedisManager(),
)


# ===== CONNECT =====
@sio.event
async def connect(sid, environ, auth):
    print(f"auth = {json.dumps(auth)}")
    user_id = auth.get("user_id") if auth else None
    if not user_id:
        print("REJECT SOCKET")
        return False  # reject connect

    user_id = int(user_id)

    # join room theo user
    await sio.enter_room(sid, f"user_{user_id}")

    # lưu redis
    # await add_user_online(user_id)

    # broadcast
    # await sio.emit(
    #     "user_online",
    #     {
    #         "user_id": user_id,
    #         "online_users": await get_online_users(),
    #     },
    # )


# ===== DISCONNECT =====
@sio.event
async def disconnect(sid):
    rooms = sio.rooms(sid)
    user_room = next((r for r in rooms if r.startswith("user_")), None)

    if not user_room:
        return

    # user_id = int(user_room.replace("user_", ""))

    # await remove_user_online(user_id)
    await sio.leave_room(sid, user_room)


# ===== GET ONLINE USERS =====
@sio.event
async def get_online_users_event(sid):
    # users = await get_online_users()
    # await sio.emit("online_users", users, to=sid)
    pass

# ===== SEND MESSAGE =====
@sio.event
async def send_message(sid, data):
    print(json.dumps(data))