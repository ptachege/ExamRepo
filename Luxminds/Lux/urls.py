from django.contrib import admin
from django.urls.conf import path
from . import views

app_name = 'Lux'

urlpatterns = [
    path("", views.index, name='index'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path('all_exams/', views.all_exams, name='all_exams'),
    path('moi_university_exams/', views.moi_university_exams,
         name='moi_university_exams'),
    path('tuk_university_exams/', views.tuk_university_exams,
         name='tuk_university_exams'),
    path('user_create_profile/', views.user_create_profile,
         name='user_create_profile'),
    path('welcome/', views.welcome, name='welcome'),
    path('view_user_profile/', views.view_user_profile, name='view_user_profile'),
    path('suggested_for_you/', views.suggested_for_you, name='suggested_for_you'),
    path('upload_papers/', views.upload_papers, name='upload_papers'),
    path('pending_approve_papers/', views.pending_approve_papers,
         name='pending_approve_papers'),
    path('approve_paper/<int:pk>/', views.approve_paper, name='approve_paper'),
    path('chat/', views.chat, name='chat'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('block_user/<int:pk>/', views.block_user, name='block_user'),
    path('view_userprofile/<int:pk>/',
         views.view_userprofile, name='view_userprofile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),


    # authentication
    path('logout_user/', views.logout_user, name='logout_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('register_user/', views.register, name='register_user'),
    # api calls
    path('all_exams_api/', views.all_exams_api, name='all_exams_api'),
]
