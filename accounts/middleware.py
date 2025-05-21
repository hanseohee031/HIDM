# accounts/middleware.py
from .models import Visit

class VisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/':           # 홈 URL 이라면
            Visit.objects.create()
        return self.get_response(request)
