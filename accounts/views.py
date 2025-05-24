from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import UserProfile
from .forms import SignupForm, UserProfileForm, AdvancedProfileForm, CategorySelectionForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core.mail import send_mail
import random
from django.contrib import messages
import json
from .models import Friendship 
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from .models import Announcement
from .forms import AnnouncementForm
from .models import UserProfile
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Category, Topic
from .forms  import TopicForm

from .forms import CategorySelectionForm  # InterestForm 대신 이걸 import


# 1. Signup View (uses Student ID, Email Verification)
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        session_code = request.session.get('email_verification_code')
        user_code     = request.POST.get('email_code', '').strip()
        email_verified = (
            session_code and
            user_code and
            str(session_code) == str(user_code)
        )

        print("SESSION CODE:", session_code)
        print("USER CODE:",    user_code)
        print("email_verified:", email_verified)

        if form.is_valid() and email_verified:
            user = form.save()
            login(request, user)

            profile, _ = UserProfile.objects.get_or_create(user=user)
            basic_topics = Topic.objects.filter(created_by__isnull=True)
            profile.selected_topics.add(*basic_topics)

            request.session.pop('email_verification_code', None)

            # ← 이 부분만 select_categories로 변경
            return redirect('select_categories')
        else:
            if not email_verified:
                form.add_error(None, "Email verification code does not match.")
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})





# 2. Send Email Verification Code (Ajax View)
@csrf_exempt
def send_verification_code_view(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id', '').strip()
        if not student_id:
            return JsonResponse({'success': False, 'msg': 'Student ID Number is required.'})

        email = f"{student_id}@hallym.ac.kr"
        code = random.randint(100000, 999999)
        request.session['email_verification_code'] = str(code)

        # Send email (Django EMAIL settings required)
        send_mail(
            subject="Your Verification Code",
            message=f"Your verification code is: {code}",
            from_email=None,  # Use DEFAULT_FROM_EMAIL from settings
            recipient_list=[email],
            fail_silently=False,
        )

        return JsonResponse({
            'success': True,
            'msg': f"A verification code has been sent to {email}. Please check your email and enter the code below."
        })

    return JsonResponse({'success': False, 'msg': 'Invalid request.'})

# 3. Login View
def login_view(request):
    if request.method == 'POST':
        student_id = request.POST['student_id']
        password = request.POST['password']
        user = authenticate(request, username=student_id, password=password)
        if user is not None:
            login(request, user)
            if not hasattr(user, 'userprofile'):
                return redirect('profile_setup')
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid Student ID Number or password.'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

# 4. Home View (with online status)
from django.contrib.auth.models import User

def home_view(request):
    profiles = UserProfile.objects.all()
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in sessions:
        data = session.get_decoded()
        uid = data.get('_auth_user_id')
        if uid:
            user_id_list.append(int(uid))
    active_user_ids = set(user_id_list)

    # 🔽 여기 추가
    total_users = User.objects.count()
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_announcements = Announcement.objects.order_by('-created_at')[:5]

    context = {
        'profiles': profiles,
        'active_user_ids': active_user_ids,
        'total_users': total_users,
        'recent_users': recent_users,
        'recent_announcements': recent_announcements,
    }

    if request.user.is_authenticated:
        context['username'] = request.user.username
        context['profile'] = getattr(request.user, 'userprofile', None)

    return render(request, 'home.html', context)




@login_required
def profile_setup_view(request):
    try:
        if hasattr(request.user, 'userprofile'):
            return redirect('home')
    except:
        pass
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('home')
    else:
        form = UserProfileForm()
    return render(request, 'profile_setup.html', {'form': form})

@login_required
def profile_update_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'profile_setup.html', {
        'form': form,
        'title': 'Update Basic Profile',
    })

@login_required
def advanced_profile_setup_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        adv_form = AdvancedProfileForm(request.POST, instance=profile)
        if adv_form.is_valid():
            adv_form.save()
            return redirect('profile')
    else:
        adv_form = AdvancedProfileForm(instance=profile)
    return render(request, 'profile_advanced_setup.html', {
        'form': adv_form,
        'title': 'Advanced Profile Setup',
    })





@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('home')
    else:
        return HttpResponse("Invalid request method.", status=400)



@login_required
def update_interests_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = CategorySelectionForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "관심 카테고리가 업데이트되었습니다.")
            return redirect('profile')
    else:
        form = CategorySelectionForm(instance=profile)

    return render(request, 'accounts/update_interests.html', {
        'form': form,
        'title': 'Update Interests',
    })

@csrf_exempt
def verify_code_ajax(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        session_code = request.session.get('email_verification_code')
        if code and session_code and code.strip() == session_code:
            return JsonResponse({'valid': True})
        else:
            return JsonResponse({'valid': False})


@login_required
def profile_view(request):
    profiles = UserProfile.objects.all()
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in sessions:
        data = session.get_decoded()
        uid = data.get('_auth_user_id')
        if uid:
            user_id_list.append(int(uid))
    active_user_ids = set(user_id_list)

    context = {
        'profiles': profiles,
        'active_user_ids': active_user_ids,
        'profile': getattr(request.user, 'userprofile', None),
    }
    return render(request, 'profile.html', context)


from django.shortcuts import render
from accounts.models import UserProfile

from .models import UserProfile, Friendship
from django.contrib.auth.decorators import login_required

@login_required
def find_friends_view(request):
    # 1) 내가 보낸 친구 요청 ID 리스트
    sent_requests_ids = list(
        Friendship.objects
        .filter(from_user=request.user, status='requested')
        .values_list('to_user_id', flat=True)
    )

    # 2) 친구 관계(accepted)인 서로의 ID 쌍을 풀고, 자기 자신 제외
    raw_pairs = Friendship.objects.filter(
        (Q(from_user=request.user) | Q(to_user=request.user)),
        status='accepted'
    ).values_list('from_user_id', 'to_user_id')
    friends_ids = set(i for pair in raw_pairs for i in pair if i != request.user.id)

    # 3) User 객체 리스트로 변환
    friends = User.objects.filter(id__in=friends_ids)

    # 4) 나에게 온 친구 요청(Friendship 객체)
    friend_requests_received = Friendship.objects.filter(
        to_user=request.user, status='requested'
    ).select_related('from_user__userprofile')

    # 5) 모든 다른 유저 프로필 (나 자신 제외)
    profiles = UserProfile.objects.exclude(user=request.user) \
                                  .prefetch_related('favorite_categories')

    # 6) Public Profile 카드용 JSON 데이터 생성
    public_profiles = {}
    for prof in profiles:
        public_profiles[prof.user.id] = {
            "nickname": prof.nickname,
            "gender": prof.get_gender_display(),
            "native_language": prof.get_native_language_display(),

            # 고급 필드는 공개 플래그 체크 후 포함
            "nationality": prof.show_nationality and prof.nationality or None,
            "major":       prof.show_major and prof.major or None,
            "personality": prof.show_personality and prof.personality or None,
            "born_year":   prof.show_born_year and prof.born_year or None,

            # interests
            "interests": [cat.name for cat in prof.favorite_categories.all()],
        }
    public_profiles_json = json.dumps(public_profiles)

    # 7) 템플릿에 모든 컨텍스트 전달
    return render(request, "accounts/find_friends.html", {
        "profiles": profiles,
        "public_profiles_json": public_profiles_json,
        "friends": friends,
        "friend_requests_received": friend_requests_received,
        "friends_ids": list(friends_ids),
        "sent_requests_ids": sent_requests_ids,
    })

@login_required
def find_topics(request):
    categories  = Category.objects.prefetch_related('topics').all()
    user_topics = request.user.userprofile.selected_topics.all()

    if request.method == 'POST':
        # a) select / deselect / clear / add_topic…
        if 'select_topic' in request.POST:
            topic = get_object_or_404(Topic, id=request.POST['topic_id'])
            request.user.userprofile.selected_topics.add(topic)

        elif 'deselect_topic' in request.POST:
            topic = get_object_or_404(Topic, id=request.POST['topic_id'])
            request.user.userprofile.selected_topics.remove(topic)

        elif 'clear_all' in request.POST:
            request.user.userprofile.selected_topics.clear()

        elif 'add_topic' in request.POST:
            form = TopicForm(request.POST)
            if form.is_valid():
                new_topic = form.save(commit=False)
                new_topic.created_by = request.user
                new_topic.save()

        # ← NEW: delete only your own topic
        elif 'delete_topic' in request.POST:
            topic = get_object_or_404(
                Topic,
                id=request.POST['topic_id'],
                created_by=request.user
            )
            topic.delete()

        return redirect('find_topics')

    form = TopicForm()
    return render(request, 'topics/find_topics.html', {
        'categories':  categories,
        'user_topics': user_topics,
        'form':        form,
    })


@login_required
def vote_topic(request, topic_id, vote_type):
    topic = get_object_or_404(Topic, id=topic_id)
    if vote_type == 'up':
        topic.upvotes.add(request.user)
        topic.downvotes.remove(request.user)
    else:
        topic.downvotes.add(request.user)
        topic.upvotes.remove(request.user)
    return redirect('find_topics')



from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@require_POST
@login_required
def friend_request_view(request):
    data = json.loads(request.body)
    userid = data.get("userid")
    if not userid or int(userid) == request.user.id:
        return JsonResponse({"success": False, "msg": "Invalid user."})
    to_user = get_object_or_404(User, id=userid)
    # 중복 요청, 이미 친구 체크
    already = Friendship.objects.filter(from_user=request.user, to_user=to_user).exists()
    if already:
        return JsonResponse({"success": False, "msg": "Already requested or already friends."})
    Friendship.objects.create(from_user=request.user, to_user=to_user, status="requested")
    return JsonResponse({"success": True})

@require_POST
@login_required
def friend_request_cancel_view(request):
    data = json.loads(request.body)
    userid = data.get("userid")
    if not userid:
        return JsonResponse({"success": False})
    Friendship.objects.filter(from_user=request.user, to_user_id=userid, status="requested").delete()
    return JsonResponse({"success": True})

@require_POST
@login_required
def friend_remove_view(request):
    data = json.loads(request.body)
    userid = data.get("userid")
    if not userid:
        return JsonResponse({"success": False})
    Friendship.objects.filter(
        ((Q(from_user=request.user) & Q(to_user_id=userid)) | (Q(from_user_id=userid) & Q(to_user=request.user))),
        status="accepted"
    ).delete()
    return JsonResponse({"success": True})

@require_POST
@login_required
def friend_accept_view(request):
    data = json.loads(request.body)
    userid = data.get("userid")
    if not userid:
        return JsonResponse({"success": False})
    fs = Friendship.objects.filter(from_user_id=userid, to_user=request.user, status="requested").first()
    if fs:
        fs.status = "accepted"
        fs.save()
    return JsonResponse({"success": True})

@require_POST
@login_required
def friend_reject_view(request):
    data = json.loads(request.body)
    userid = data.get("userid")
    if not userid:
        return JsonResponse({"success": False})
    Friendship.objects.filter(from_user_id=userid, to_user=request.user, status="requested").delete()
    return JsonResponse({"success": True})
def is_allowed_user(user):
    return user.is_authenticated and user.username in ['admin', 'HID', '개발자']





def announcement_list(request):
    allowed_users = ['admin', 'HID', '개발자']

    # 추가: 검색어, 검색타입 받기
    q = request.GET.get('q', '').strip()
    search_type = request.GET.get('search_type', 'title')

    announcements = Announcement.objects.all()

    # 추가: 검색 필터 적용
    if q:
        if search_type == 'title':
            announcements = announcements.filter(title__icontains=q)
        elif search_type == 'content':
            announcements = announcements.filter(content__icontains=q)
        elif search_type == 'all':
            announcements = announcements.filter(
                Q(title__icontains=q) | Q(content__icontains=q)
            )

    # 추가: 최신순 정렬
    announcements = announcements.order_by('-created_at')

    return render(request, 'accounts/announcement_list.html', {
        'announcements': announcements,
        'allowed_users': allowed_users,
    })


from django.core.exceptions import PermissionDenied

def is_allowed_user(user):
    allowed_nicknames = ['admin', '개발자', 'HID']
    # user가 인증된 상태인지, userprofile이 있는지 등도 체크 가능
    if not user.is_authenticated:
        return False
    # 닉네임이 allowed_nicknames 목록에 있으면 True 반환
    try:
        return user.userprofile.nickname in allowed_nicknames
    except AttributeError:
        # userprofile이 없으면 권한 없음 처리
        return False


def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    announcement.views += 1
    announcement.save(update_fields=['views'])
    return render(request, 'accounts/announcement_detail.html', {'announcement': announcement})

@login_required
def announcement_create(request):
    if not is_allowed_user(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            return redirect('announcement_detail', pk=announcement.pk)
    else:
        form = AnnouncementForm()
    return render(request, 'accounts/announcement_form.html', {'form': form})

@login_required
def announcement_edit(request, pk):
    if not is_allowed_user(request.user):
        raise PermissionDenied
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcement_detail', pk=announcement.pk)
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'accounts/announcement_form.html', {'form': form})

@login_required
def announcement_delete(request, pk):
    if not is_allowed_user(request.user):
        raise PermissionDenied
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        announcement.delete()
        return redirect('announcement_list')
    return render(request, 'accounts/announcement_confirm_delete.html', {'announcement': announcement})







@login_required
def select_categories_view(request):
    # 프로필 가져오기 (없으면 생성)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # 이미 선택된 카테고리가 있으면 프로필 페이지로
    if profile.favorite_categories.exists():
        return redirect('profile')

    if request.method == 'POST':
        form = CategorySelectionForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CategorySelectionForm()

    return render(request, 'accounts/select_categories.html', {'form': form})
def ai_matching(request):
    # 템플릿만 렌더링할 거니까, 비어있어도 상관없습니다.
    return render(request, 'accounts/ai_matching.html')
