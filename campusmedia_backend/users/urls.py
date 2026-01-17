from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('', views.get_all_users, name='users-list'),
    path('<int:user_id>/', views.get_user, name='user-detail'),
    path('update-staff-details/', views.update_staff_details, name='update-staff-details'),
    path('update-student-details/', views.update_student_details, name='update-student-details'),
    path('announcements/create/', views.create_announcement, name='create-announcement'),
    path('announcements/', views.get_announcements, name='announcements-list'),
]
