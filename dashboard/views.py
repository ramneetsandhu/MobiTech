from re import template
import re
from turtle import update
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.shortcuts import render, redirect
import qrcode
from accounts.models import User
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
import os
import jwt
from datetime import date, datetime
from accounts.models import User
from django.shortcuts import get_object_or_404
from .forms import UserUpdateForm
from django.contrib import messages

QR_PATH = os.path.join(settings.BASE_DIR, 'public')


class DashboardView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("/accounts/login")
        
        # encoded_jwt = 
        user = request.user
        username = request.user.username
        user_obj = SocialAccount.objects.filter(user=user).values('extra_data')[0]
        cust_info = {
            'username': username,
            'name': user.name,
            'phone': user.phone,
            'address': user.address,
            'city' : user.city,
            'extra_data' : user_obj['extra_data']
        }
        secure_code = jwt.encode({"customer_data": cust_info}, "secret", algorithm="HS256")
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=2,
        )
        data = {
            'secure_code' : secure_code
        }
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_name = username + ".png"
        sav_path = QR_PATH + "/" + img_name
        img.save(sav_path)
        context_data = {"qrcode": img_name }
        return render(request, template_name='dashboard/home.html', context=context_data)


class ProfileView(View):
    template_name = 'dashboard/profile.html'

    def get(self, request):
        pk = request.user.id
        profile_obj = get_object_or_404(User, id=pk)
        context_data = {}
        context_data['profile_obj'] = profile_obj
        return render(request, self.template_name, context_data)
    
    def post(self, request):
        
        u_form = UserUpdateForm(request.POST,request.FILES, instance=request.user)
        if u_form.is_valid():
            messages.success(request,'Your Profile has been updated!')
            u_form.save()
            return redirect('profile')
        else:
            print(u_form.errors)
        context={'form': u_form}
        return render(request, self.template_name,context )
