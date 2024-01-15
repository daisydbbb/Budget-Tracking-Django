from django.urls import path
from .views import RegistrationView, UserNameValidationView, EmailValidationView, VerificationView, loginView, logoutView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('user-validation', csrf_exempt(UserNameValidationView.as_view()), name='user-validation'),
    path('email-validation', csrf_exempt(EmailValidationView.as_view()), name='email-validation'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('login', loginView.as_view(), name='login'),
    path('logout', logoutView.as_view(), name='logout')
]
