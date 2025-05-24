from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),  # 프로필 페이지 추가
    path('setup-profile/', views.profile_setup_view, name='profile_setup'),
    path('update-profile/', views.profile_update_view, name='profile_update'),
    path('advanced-profile/', views.advanced_profile_setup_view, name='profile_advanced'),
    path('signup/categories/', views.select_categories_view, name='select_categories'),

    path('interests/update/', views.update_interests_view, name='update_interests'),

    # Email verification for student ID
    path('send-verification-code/', views.send_verification_code_view, name='send_verification_code'),
    path('verify-code/', views.verify_code_ajax, name='verify_code_ajax'), 

    path('delete_account/', views.delete_account_view, name='delete_account'),
    path('find-friends/', views.find_friends_view, name='find_friends'),
    path('friend-request/', views.friend_request_view, name='friend_request'),
    path('friend-request-cancel/', views.friend_request_cancel_view, name='friend_request_cancel'),
    path('friend-remove/', views.friend_remove_view, name='friend_remove'),
    path('friend-accept/', views.friend_accept_view, name='friend_accept'),
    path('friend-reject/', views.friend_reject_view, name='friend_reject'),
    path('announcement/', views.announcement_list, name='announcement_list'),
    path('announcement/create/', views.announcement_create, name='announcement_create'),
    path('announcement/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('announcement/<int:pk>/edit/', views.announcement_edit, name='announcement_edit'),
    path('announcement/<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),
    # Find Topics feature
    path('find-topics/', views.find_topics, name='find_topics'),
    path(
        'topic/<int:topic_id>/vote/<str:vote_type>/',
        views.vote_topic,
        name='vote_topic'
    ),

]


