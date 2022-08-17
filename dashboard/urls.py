from django.urls import path
from .views import DashboardView, ProfileView

urlpatterns = [
    path('home/',  DashboardView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile')
]