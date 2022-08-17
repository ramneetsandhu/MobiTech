from django.contrib import admin
from .models import User
# Register your models here.
# admin.site.register(User)

class UserAdmin(admin.ModelAdmin):
    list_display= ['username', 'first_name', 'last_name']

admin.site.register(User, UserAdmin)