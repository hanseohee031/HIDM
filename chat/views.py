from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .matchmaker import find_match
from django.http import JsonResponse
from django.urls import reverse
import redis
from .matchmaker import QUEUE_KEY, MAP_KEY
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import HttpResponse
from .import matchmaker
from django.views.decorators.csrf import csrf_exempt

from accounts.models import UserProfile

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from accounts.models import User, Friendship
from django.db.models import Q


@login_required
def dm_chat_room(request, nickname):
    user = request.user
    friend_profile = get_object_or_404(UserProfile, nickname=nickname)
    friend = friend_profile.user

    # 친구 관계 확인
    if not Friendship.objects.filter(
        ((Q(from_user=user) & Q(to_user=friend)) | (Q(from_user=friend) & Q(to_user=user))) & Q(status='accepted')
    ).exists():
        raise Http404("You are not friends.")

    return render(request, 'chat/dm_chat_room.html', {'friend_profile': friend_profile})




@csrf_exempt
@login_required
def cancel_waiting(request):
    """
    현재 로그인한 사용자를 매칭 대기열에서 제거합니다.
    GET/POST 모두 OK하도록 csrf_exempt 처리했습니다.
    """
    username = request.user.username
    matchmaker.remove_user(username)    # 실제 matchmaker.py 안 함수 이름에 맞춰서 호출
    return JsonResponse({'status': 'cancelled'})

redis_client = redis.Redis(host='localhost', port=6379, db=0)
QUEUE_KEY = 'chat_waiting_queue'


@staff_member_required
def show_waiting_queue(request):
    # Redis에서 대기 리스트 불러오기 (예: list key = 'chat_waiting')
    r = redis.Redis()
    waiting = r.lrange('chat_waiting', 0, -1)  # bytes 리스트
    # UTF-8 문자열로 디코딩
    waiting = [u.decode('utf-8') for u in waiting]
    return HttpResponse(
        '<br>'.join(waiting),
        content_type='text/html; charset=utf-8'    )

@login_required
def match_request_view(request):
    room_name = find_match(request.user.username)
    if room_name:
        url = reverse('chat_room', args=[room_name])
        return JsonResponse({'room_url': url})
    return JsonResponse({'room_url': None})
@login_required
def chat_room(request):
    return render(request, 'chat.html')

# Create your views here.
@login_required
def room_view(request, room_name):
    return render(request, 'chat.html', {'room_name': room_name})

@login_required
def waiting_view(request):
    """
    사용자에게 waiting.html을 띄워 주는 뷰.
    스크립트가 3초마다 /match/를 폴링합니다.
    """
    return render(request, 'waiting.html')


@login_required
def cancel_waiting(request):
    username = request.user.username
    redis_client.lrem(QUEUE_KEY, 0, username)
    redis_client.hdel(MAP_KEY, username)
    return redirect('home')


@staff_member_required  # 로그인 + is_staff=True 사용자만 접근 가능
def show_waiting_queue(request):
    queue = redis_client.lrange(QUEUE_KEY, 0, -1)
    usernames = [u.decode('utf-8') for u in queue]
    return JsonResponse({'waiting': usernames})
