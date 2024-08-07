from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.core.mail import EmailMessage
import threading
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import TokenGenerator, generate_token

User = get_user_model()

class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        confirm_password = request.POST.get('pass2')
        name = request.POST.get('name')
        mobilenumber = request.POST.get('mobilenumber')

        if password != confirm_password:
            messages.warning(request, 'Passwords do not match')
            return render(request, 'pages/register.html')

        try:
            if User.objects.get(email=email):
                messages.warning(request, 'Email already exists')
                return render(request, 'pages/register.html')
        except User.DoesNotExist:
            pass

        user = User.objects.create_user(email=email, password=password, name=name, mobilenumber=mobilenumber)
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        email_subject = 'Activate your account'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = generate_token.make_token(user)
        message = render_to_string('inc/activate.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': uid,
            'token': token
        })
        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
        EmailThread(email_message).start()
        messages.success(request, 'Activate your account by clicking on the link sent to your email')
        return render(request, 'pages/login.html')

    return render(request, 'pages/register.html')

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully')
            return redirect('login_view')
        return render(request, 'inc/activationfail.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pass1']
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            print(user)
            messages.success(request, 'Logged in successfully')
            return render(request, 'pages/index.html')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('logout_view')

    return render(request, 'pages/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return render(request, 'pages/login.html')

class RequestResetEmailView(View):
    def get(self, request):
        return render(request, 'pages/request-reset-email.html')

    def post(self, request):
        email = request.POST['email']
        user = User.objects.filter(email=email)

        if user.exists():
            user = User.objects.get(email=email)
            current_site = get_current_site(request)
            email_subject = 'Reset your password'
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            message = render_to_string('inc/reset-user-password.html', {
                'domain': '127.0.0.1:8000',
                'uid': uidb64,
                'token': token
            })
            email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
            email_message.send()
            messages.info(request, 'Password reset link has been sent to your email')
        return render(request, 'pages/request-reset-email.html')
    
class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.warning(request, 'Password reset link invalid or expired')
                return render(request, 'pages/request-reset-email.html')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, UnicodeDecodeError):
            pass
        return render(request, 'pages/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']

        if password != confirm_password:
            messages.warning(request, 'Passwords do not match')
            return render(request, 'pages/set-new-password.html', context)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect('login_view')

        except (TypeError, ValueError, OverflowError, User.DoesNotExist, UnicodeDecodeError):
            messages.error(request, 'Something went wrong')
            return render(request, 'pages/set-new-password.html', context)

  
