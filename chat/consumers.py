import json
import os
import asyncio
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from . import matchmaker

# 로그 파일 경로 (JSONL 포맷)
LOG_JSONL = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'logs',
    'chat.jsonl'
)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # URL 라우팅에서 room_name 꺼내기
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # 그룹에 자신 추가
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        # 매칭 시스템에서 사용자 제거
        username = self.scope['user'].username
        await database_sync_to_async(matchmaker.remove_user)(username)

        # 그룹에서 자신 제거
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        # 클라이언트로부터 JSON 메시지 수신
        data = json.loads(text_data)
        message     = data.get('message')
        sender      = data.get('sender')
        profile_img = data.get('profile_img')

        # 그룹에 메시지 브로드캐스트
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'profile_img': profile_img,
            }
        )

    async def chat_message(self, event):
        # 클라이언트로 전송
        await self.send(text_data=json.dumps({
            'message':     event['message'],
            'sender':      event['sender'],
            'profile_img': event['profile_img'],
        }))

        # JSONL 포맷으로 로그 기록
        record = {
            'timestamp':   datetime.utcnow().isoformat() + 'Z',
            'room':        self.room_group_name,
            'sender':      event['sender'],
            'message':     event['message'],
            'profile_img': event['profile_img'],
        }
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._write_jsonl, record)

    def _write_jsonl(self, record: dict):
        """한 줄에 JSON 객체를 기록하는 JSONL 포맷 로그 쓰기"""
        os.makedirs(os.path.dirname(LOG_JSONL), exist_ok=True)
        with open(LOG_JSONL, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
