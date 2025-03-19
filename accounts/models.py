from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)
    profile_pic = models.ImageField(upload_to='accounts/profile_pics', null=True, blank=True)
    
    # Assign the custom manager
    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []  

    def __str__(self):
        return self.phone_number
