# accounts/admin.py
from django.contrib import admin
from .models import UserProfile
from .models import ChatRequest

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',     # 보통 user.username 필드를 학생번호로 쓰시는 경우
        'nickname',
        'gender',
        'native_language',
        'nationality',
        'major',
        'born_year',
        'personality',
        'bio_short',
        'display_interests',
    )
    list_per_page = 50      # 페이지 당 보여줄 행 수
    search_fields = ('user__username','nickname','nationality')
    
    def student_id(self, obj):
        return obj.user.username
    student_id.short_description = 'Student ID'
    
    def bio_short(self, obj):
        return obj.bio[:20] + ('…' if len(obj.bio)>20 else '')
    bio_short.short_description = 'Bio'
    
    def display_interests(self, obj):
        qs = obj.interests.all()[:5]
        return ", ".join(i.name for i in qs)
    display_interests.short_description = 'My Interests (5)'



# ChatRequest 모델 등록
@admin.register(ChatRequest)
class ChatRequestAdmin(admin.ModelAdmin):
    list_display = (
        'sender', 'receiver',
        'status', 'slot1', 'slot2', 'slot3', 'chosen_slot',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = (
        'sender__username',
        'receiver__username',
    )
    readonly_fields = ('created_at', 'updated_at')
