# Import necessary Django modules and classes for user authentication and email handling
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from .forms import RegistrationForm
from .tasks import send_verification_email, send_password_reset_email

def register_view(request):
    # Handle user registration
    if request.method == 'POST':
        # Retrieve user input from the form
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate password and username/email uniqueness
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')  # Username conflict
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')  # Email conflict
            else:
                # Create a new user and deactivate the account for email verification
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.is_active = False  # User must activate account via email link
                user.save()

                # Generate token and UID for email verification
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                # Prepare email content for activation
                mail_subject = 'Activate your account'
                html_message = render_to_string('AuthSys/activation_email.html', {
                    'user': user,
                    'uid': uid,
                    'token': token,
                    'domain': request.get_host(),
                })

                # Send verification email asynchronously
                send_verification_email.delay(mail_subject, html_message, [user.email])

                messages.success(request, 'Please check your email to activate your account.')  # Success message
                return redirect('AuthSys:login')  # Redirect to login page
        else:
            messages.error(request, 'Passwords do not match.')  # Password mismatch error
    return render(request, 'AuthSys/register.html')  # Render registration form

def activate_view(request, uidb64, token):
    # Handle account activation using the provided UID and token
    try:
        # Decode UID to get user ID
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)  # Retrieve user based on ID
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None  # Handle invalid UID or user not found

    # Verify token and activate the user account
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # Activate the user account
        user.save()
        messages.success(request, 'Your account has been activated successfully!')  # Success message
        return redirect('AuthSys:login')  # Redirect to login page
    else:
        messages.error(request, 'Activation link is invalid!')  # Invalid activation link error
        return redirect('Home:home')  # Redirect to home page

def login_view(request):
    # Handle user login
    if request.method == 'POST':
        # Retrieve user input for login
        username = request.POST['username']
        password = request.POST['password']

        # Print values to console for debugging
        print(f"Login Attempt: Username: {username}, Password: {password}")

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        # Check if the user is authenticated and active
        if user is not None:
            if user.is_active:
                login(request, user)  # Log the user in
                return redirect('Home:home')  # Redirect to home page
            else:
                messages.error(request, 'Your account is not activated. Please check your email for the activation link.')  # Account not activated error
        else:
            messages.error(request, 'Invalid login credentials')  # Invalid credentials error
    return render(request, 'AuthSys/login.html')  # Render login form

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    # Custom view for password reset confirmation
    template_name = 'AuthSys/custom_password_reset_confirm.html'  # Custom template for password reset confirmation
    form_class = SetPasswordForm  # Use Django's built-in form for setting password
    success_url = reverse_lazy('AuthSys:password_reset_complete')  # Redirect after successful password reset

    def form_valid(self, form):
        # Log the new password for debugging purposes
        new_password = form.cleaned_data.get('password1')
        print(f"New Password: {new_password}")  # Print new password

        # Call the parent class's form_valid method to proceed with the password reset
        return super().form_valid(form)

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    # Custom view for password reset completion
    template_name = 'AuthSys/password_reset_complete.html'  # Custom template for completion
    success_url = reverse_lazy('AuthSys:login')  # Redirect to login page after completion

def forgot_password_view(request):
    # Handle the forgot password functionality
    if request.method == 'POST':
        email = request.POST.get('email')  # Retrieve email input from the form
        if email:
            try:
                user = User.objects.get(email=email)  # Attempt to retrieve user by email

                # Generate UID and token for password reset
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                # Build password reset URL
                reset_url = request.build_absolute_uri(reverse('AuthSys:custom_password_reset_confirm', kwargs={
                    'uidb64': uidb64,
                    'token': token,
                }))

                # Prepare email content for password reset
                mail_subject = 'Reset your password'
                html_message = render_to_string('AuthSys/password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url,
                    'domain': request.get_host(),
                    'protocol': 'https' if request.is_secure() else 'http',
                })

                # Send password reset email asynchronously
                send_password_reset_email.delay(mail_subject, html_message, [user.email])

                messages.success(request, 'Password reset email has been sent.')  # Success message
                return redirect('AuthSys:login')  # Redirect to login page
            except User.DoesNotExist:
                messages.error(request, 'No user with this email address.')  # User not found error
        else:
            messages.error(request, 'Please enter an email address.')  # No email provided error
    return render(request, 'AuthSys/forgot_password.html')  # Render forgot password form

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    # Custom view for password reset completion
    template_name = 'AuthSys/password_reset_mail_send.html'  # Custom template for email sent confirmation
    success_url = reverse_lazy('AuthSys:login')  # Redirect to login page after completion
