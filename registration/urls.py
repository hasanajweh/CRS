# registration/urls.py

from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import course_search
from django.contrib.auth.views import LogoutView
from .views import custom_logout

urlpatterns = [
    # App-specific URLs, like:
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='user_login'),  # This 'login' URL is now within the 'registration/' path
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('search/', course_search, name='course_search'),
    path('home/', views.home, name='home'),
    path('logout/', views.custom_logout, name='logout'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/schedule/', views.course_schedule, name='course_schedule'),
    
    ]

