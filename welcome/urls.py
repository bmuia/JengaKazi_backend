from django.urls import path
from .views import WelcomeView

urlpatterns = [
    path('', WelcomeView.as_view(),name='welcome-view'),
]
