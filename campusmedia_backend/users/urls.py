from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('', views.get_all_users, name='users-list'),
    path('<int:user_id>/', views.get_user, name='user-detail'),
]
