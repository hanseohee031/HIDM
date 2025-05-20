
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path("admin/", admin.site.urls),
    path('accounts/', include('accounts.urls')),  # ← prefix 추가!
    path('', include('chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf import settings
from django.conf.urls.static import static

# DEBUG=True인 개발 환경에서만 /static/ 파일을 settings.STATICFILES_DIRS의 경로에서 서빙
urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.BASE_DIR / "static",
)
