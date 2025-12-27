from app.core.redis import redis_client

ONLINE_USERS_KEY = "online_users"


async def add_user_online(user_id: int):
    await redis_client.sadd(ONLINE_USERS_KEY, user_id)


async def remove_user_online(user_id: int):
    await redis_client.srem(ONLINE_USERS_KEY, user_id)


async def get_online_users():
    users = await redis_client.smembers(ONLINE_USERS_KEY)
    return list(map(int, users))
