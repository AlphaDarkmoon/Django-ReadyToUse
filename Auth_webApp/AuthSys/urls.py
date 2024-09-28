from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetConfirmView, CustomPasswordResetCompleteView

app_name = 'AuthSys'  # Set the application namespace for URL namespacing

urlpatterns = [
    path('register/', views.register_view, name='register'),  # URL for user registration
    path('login/', views.login_view, name='login'),  # URL for user login
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),  # URL for password recovery
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # URL for password reset confirmation
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),  # URL for completion of password reset process
    path('activate/<uidb64>/<token>/', views.activate_view, name='activate'),  # URL for activating user account
    path('reset-password/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='custom_password_reset_confirm'),  # URL for custom password reset confirmation
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # URL for user logout
]
