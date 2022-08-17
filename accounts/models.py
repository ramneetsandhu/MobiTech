from django.db import models
from PIL import Image
import os
from django.conf import settings
# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager


IMG_PATH = os.path.join(settings.BASE_DIR, 'public', 'img')

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractUser):
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=255)
    profile_photo = models.ImageField(upload_to='img',null=True,blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=12, null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD ='email' 
    REQUIRED_FIELDS =['username']

    objects = UserManager()

    class Meta:
        db_table = "accounts_user"
        verbose_name = "user"
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_photo:
            img = Image.open(self.profile_photo.path)
            if img.mode in ("RGBA", "P"): img = img.convert("RGB")
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_photo.path)
