from django.urls import path
from .views import waiting_view, match_request_view, room_view, cancel_waiting
from .views import show_waiting_queue
from .views import cancel_waiting

urlpatterns = [
    path('chat/waiting/', waiting_view,       name='waiting'),
    path('match/',         match_request_view, name='match'),
    path('match/cancel/',  cancel_waiting,     name='cancel_waiting'),
    path('chat/room/<str:room_name>/', room_view,    name='chat_room'),
    path('admin/waiting/', show_waiting_queue, name='show_waiting_queue'),
]
