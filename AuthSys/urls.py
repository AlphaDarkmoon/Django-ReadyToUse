from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetConfirmView,CustomPasswordResetCompleteView

app_name = 'AuthSys'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', views.activate_view, name='activate'),  # Add this line
    path('reset-password/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='custom_password_reset_confirm'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]
