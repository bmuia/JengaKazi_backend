from django.urls import path
from .views import (
    SendOtpView,
    JobSeekerRegistrationView,
    EmployerRegistrationView,
    LoginView,
    UpdateProfileView
)

urlpatterns = [
    path('send-otp/', SendOtpView.as_view(), name='send-otp'),
    path('register/job-seeker/', JobSeekerRegistrationView.as_view(), name='job-seeker-registration'),
    path('register/employer/', EmployerRegistrationView.as_view(), name='employer-registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/update/', UpdateProfileView.as_view(), name='update-profile'),
]
