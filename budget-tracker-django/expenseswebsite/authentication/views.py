from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.urls import reverse

from .utils import account_activation_token
from django.contrib.auth import authenticate, login, logout

class UserNameValidationView(View):
  def post(self, request):
    data = json.loads(request.body)
    username = data['username']
    if not str(username).isalnum():
      return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)

    if User.objects.filter(username=username).exists():
      return JsonResponse({'username_error': 'Username already exist, please choose another one'}, status=400)

    return JsonResponse({'username_isValid': True})

class EmailValidationView(View):
  def post(self, request):
    data = json.loads(request.body)
    email = data['email']
    if not validate_email(email):
      return JsonResponse({'email_error': 'Email address not valid'}, status=400)

    if User.objects.filter(email=email).exists():
      return JsonResponse({'email_error': 'Email already exist, please choose another one'}, status=400)

    return JsonResponse({'email_isValid': True})


class RegistrationView(View):
  def get(self, request):
    return render(request, 'authentication/register.html')

  def post(self, request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']

    context ={
      'fieldValues': request.POST
    }

    if not User.objects.filter(username=username) and not User.objects.filter(email=email):

      if len(password) < 6:
        messages.error(request, 'Password too short')
        return render(request, 'authentication/register.html', context)
      user = User.objects.create_user(username=username, email=email)
      user.set_password(password)
      user.is_active = False
      user.save()

      # send email to registered user email address
      uidb64= urlsafe_base64_encode(force_bytes(user.pk))
      domain = get_current_site(request).domain
      link = reverse('activate', kwargs={'uidb64':uidb64, 'token': account_activation_token.make_token(user)})

      activate_url = 'http://'+domain+link
      email_subject = 'Activate your account'
      email_body = 'Hi '+user.username+ ', Please use this link to verify your account\n' + activate_url
      email = EmailMessage(
          email_subject,
          email_body,
          "nonreply@semycolon.com",
          [email],
      )
      email.send(fail_silently=False)
      messages.success(request, 'Registration successful')
      return render(request, 'authentication/register.html')

    return render(request, 'authentication/register.html')


class VerificationView(View):
  def get(self, request, uidb64, token):
    try:
      user_id =force_str(urlsafe_base64_decode(uidb64))
      user = User.objects.get(pk=user_id)

      # check if the user is activated
      # if not account_activation_token.check_token(user, token):
      #     return redirect('login'+'?message='+'User already activated')
      if user.is_active:
          messages.success(request, 'Account already activated')
          return redirect('login')

      user.is_active = True
      user.save()
      messages.success(request, 'Account activated successfully')
      return redirect('login')

    except Exception as ex:
      pass
    return redirect('login')


class loginView(View):
  def get(self, request):
    return render(request, 'authentication/login.html')

  def post(self, request):
    username=request.POST['username']
    password=request.POST['password']

    if username and password:
      user = authenticate(username=username, password=password)

      if user:
        if user.is_active:
          login(request, user)
          messages.success(request, 'Welcome back!')
          return redirect('expenses')

        messages.error(request, 'Account not activated, please check your email!')
        return render(request, 'authentication/login.html')
      else:
        messages.error(request, ' Username and password did not match, please try again!')
        return render(request, 'authentication/login.html')

    messages.error(request, ' Invlid username or password, please try again!')
    return render(request, 'authentication/login.html')

class logoutView(View):
  def post(self, request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('login')
