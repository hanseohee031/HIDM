from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.cache import cache
from .models import UserProfile

@receiver(m2m_changed, sender=UserProfile.favorite_categories.through)
def invalidate_cache_on_interest_change(sender, instance, **kwargs):
    user_id = instance.user.id
    cache.delete(f'ai_match_results_{user_id}')
    print(f"🧹 AI 캐시 삭제됨: 사용자 {user_id}")
