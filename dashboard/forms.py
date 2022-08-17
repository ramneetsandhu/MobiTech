
from django import forms
from accounts.models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','name', 'phone', 'address', 'city', 'profile_photo']
