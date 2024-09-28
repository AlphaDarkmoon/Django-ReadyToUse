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
from django.contrib.auth.views import PasswordResetConfirmView
from .forms import RegistrationForm


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Print values to console
        print(f"Registering User: Username: {username}, Email: {email}, Password: {password1}")

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.is_active = False  # Deactivate account until email verification
                user.save()

                # Send verification email
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                mail_subject = 'Activate your account'
                html_message = render_to_string('AuthSys/activation_email.html', {
                    'user': user,
                    'uid': uid,
                    'token': token,
                    'domain': request.get_host(),
                })
                plain_message = strip_tags(html_message)

                send_mail(
                    mail_subject,
                    plain_message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    html_message=html_message
                )

                messages.success(request, 'Please check your email to activate your account.')
                return redirect('AuthSys:login')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'AuthSys/register.html')


def activate_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully!')
        return redirect('AuthSys:login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('Home:home')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Print values to console
        print(f"Login Attempt: Username: {username}, Password: {password}")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('Home:home')
            else:
                messages.error(request, 'Your account is not activated. Please check your email for the activation link.')
        else:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'AuthSys/login.html')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'AuthSys/custom_password_reset_confirm.html'  # Point to your custom template
    form_class = SetPasswordForm  # Use Django's built-in form to set the password
    success_url = reverse_lazy('AuthSys:password_reset_complete')  # Where to redirect after a successful reset

    def form_valid(self, form):
        # You can add custom logic here if necessary
        return super().form_valid(form)


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                user = User.objects.get(email=email)  # Get the user by email

                # Generate UID and token
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                # Build the password reset URL
                reset_url = request.build_absolute_uri(reverse('AuthSys:custom_password_reset_confirm', kwargs={
                    'uidb64': uidb64,  # Make sure uidb64 and token are passed correctly
                    'token': token,
                }))

                # Prepare email content
                mail_subject = 'Reset your password'
                html_message = render_to_string('AuthSys/password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url,
                    'domain': request.get_host(),
                    'protocol': 'https' if request.is_secure() else 'http',
                })

                send_mail(
                    mail_subject,
                    html_message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    html_message=html_message,
                )

                messages.success(request, 'Password reset email has been sent.')
                return redirect('AuthSys:login')
            except User.DoesNotExist:
                messages.error(request, 'No user with this email address.')
        else:
            messages.error(request, 'Please enter an email address.')
    return render(request, 'AuthSys/forgot_password.html')


from django.contrib.auth.views import PasswordResetCompleteView
from django.urls import reverse_lazy

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'AuthSys/password_reset_mail_send.html'
    success_url = reverse_lazy('AuthSys:login')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'AuthSys/password_reset_complete.html'  # Point to your custom template
    success_url = reverse_lazy('AuthSys:login')  # Redirect to the login page or any other page after reset
