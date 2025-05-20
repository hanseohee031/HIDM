# chat/room_manager.py
import uuid
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)
ROOM_HASH_KEY = 'chat_rooms'

def create_room():
    room_name = uuid.uuid4().hex[:8]             # 8자리 랜덤 방 ID
    password  = uuid.uuid4().hex[:6]             # 6자리 랜덤 비번
    redis_client.hset(ROOM_HASH_KEY, room_name, password)
    return room_name, password

def check_password(room_name, pw):
    stored = redis_client.hget(ROOM_HASH_KEY, room_name)
    return stored and stored.decode() == pw

def delete_room(room_name):
    redis_client.hdel(ROOM_HASH_KEY, room_name)
    redis_client.delete(f'room_users:{room_name}')
