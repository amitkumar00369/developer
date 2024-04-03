from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils import timezone

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
  
   
    mobile_no = models.CharField(max_length=15, unique=True)
   
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    profile_image=models.CharField(max_length=128,blank=True)
    Designation=models.CharField(max_length=80,blank=True)

    
   
    # motors_assign=models.CharField(max_length=255,null=True,blank=True,default=False)
    username = None

    objects = CustomUserManager()
    # status = models.BooleanField(default=False)  # Default status is False
    # admin_approval = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_no']

    def __str__(self):
        return self.email


# CustomUser._meta.get_field('groups').remote_field.related_name = 'customuser_groups'
# CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'customuser_user_permissions'
from django.contrib.auth.hashers import make_password


class AdminTables(models.Model):
    email = models.EmailField(unique=True, default=True)
    password = models.CharField(max_length=128, default=True)

    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


# Admin Status Table not used Table -------------------------------------------------------------------
class AdminStatusTable(models.Model):
    email = models.EmailField(unique=True)
    is_approved = models.BooleanField(default=False)


# Token table for user_login and admin login

class UserTokenTable(models.Model):
    user_id = models.IntegerField(unique=True)
    token_store = models.CharField(max_length=255)
    email = models.EmailField(max_length=40, default=False)


class AdminTokenTable(models.Model):
    user_id = models.IntegerField()
    token_store = models.CharField(max_length=255)
    email = models.EmailField(max_length=40, default=False)


# OTP verifaction Table
class OTPVerification_TABLE(models.Model):
    email = models.EmailField(max_length=40, default=False)
    otp = models.CharField(max_length=4, default=False)


class profile_image_table(models.Model):
    profile_image = models.ImageField(upload_to='image/', blank=True, null=True)
    video_link=models.FileField(upload_to='videos/', blank=True, null=True)
    ppts=models.FileField(upload_to='pdf/',blank=True,null=True)
    



class Course_table(models.Model):
    id=models.AutoField(primary_key=True)
    weeks=models.CharField(max_length=20,blank=True,default=None)
    text=models.JSONField(default=list,null=True,blank=True)
    heading=models.CharField(max_length=255,default=list)
    video=models.CharField(max_length=128,blank=True)
    PPT=models.CharField(max_length=128,blank=True)
    course_name=models.CharField(max_length=255,blank=True)
    course_id=models.CharField(max_length=20,blank=True)
    headings=models.CharField(max_length=255,blank=True)
    
    date = models.DateField(default=timezone.now, blank=True)
    time = models.TimeField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        # Update date and time fields to current date and time on every save
        self.date = timezone.now().date()
        self.time = timezone.now().time()
        super().save(*args, **kwargs)
    

    









    
    