from django.urls import path
from .views import verificationAPI


app_name = 'accounts'
urlpatterns = [
    path('verification/', verificationAPI.as_view(), name='verification-token')
]