# django_chat/chat/matchmaker.py
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

QUEUE_KEY = "chat_waiting_queue"
MAP_KEY   = "chat_match_map"   # 매칭 맵 해시

def find_match(username: str):
    print(f"[MATCHER] find_match called for: {username}")
    # 1) 이미 매핑 맵에 기록된 방 확인
    room = redis_client.hget(MAP_KEY, username)
    if room:
        room_name = room.decode('utf-8')
        redis_client.hdel(MAP_KEY, username)
        print(f"[MATCHER] existing mapping for {username} -> {room_name}")
        return room_name

    # 2) 대기 큐 순회
    while True:
        other = redis_client.lpop(QUEUE_KEY)
        if not other:
            print(f"[MATCHER] no other in queue for {username}")
            break
        other = other.decode('utf-8')
        print(f"[MATCHER] popped from queue: {other}")
        if other != username:
            room_name = "__".join(sorted([username, other]))
            redis_client.hset(MAP_KEY, username, room_name)
            redis_client.hset(MAP_KEY, other,   room_name)
            print(f"[MATCHER] matched {username} <> {other} -> {room_name}")
            return room_name

    # 3) 매칭 실패
    redis_client.rpush(QUEUE_KEY, username)
    print(f"[MATCHER] requeued {username}")
    return None


def add_user(username: str):
    redis_client.rpush(QUEUE_KEY, username)

def remove_user(username: str):
    """
    대기 큐와 매칭 맵에서 username을 완전히 제거합니다.
    """
    # 1) 대기 큐(list)에서 username 제거
    #    count=0 이면 큐에 있는 모든 동일 값(username)을 삭제
    redis_client.lrem(QUEUE_KEY, 0, username)
    # 2) 이미 매핑된 방(map)에서도 삭제
    redis_client.hdel(MAP_KEY, username)
