from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils import timezone

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
  
   
    mobile_no = models.CharField(max_length=15, unique=True)
   
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    profile_image=models.CharField(max_length=128,blank=True,null=True,default=None)
    Designation=models.CharField(max_length=80,blank=True)
    level=models.CharField(max_length=128,blank=True)
    No_of_Course=models.CharField(max_length=255, default='')
    Course_id=models.CharField(max_length=255, default=list)
    Course_name=models.CharField(max_length=255, default=list)
    

    
   
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
    weeks=models.CharField(max_length=20,blank=True,default=None,null=True)
    text=models.JSONField(default=list,null=True,blank=True)
    heading=models.CharField(max_length=255,default=list)
    video=models.FileField(upload_to='videos/', blank=True,null=True)
    PPT=models.FileField(upload_to='pdf/',blank=True,null=True)
    course_name=models.CharField(max_length=255,default='',blank=True,null=True)
    course_id=models.IntegerField(default=0)
    headings=models.CharField(max_length=255,blank=True)
    active=models.BooleanField(default=False)
    archive=models.BooleanField(default=False)
    
    date = models.DateField(default=timezone.now, blank=True)
    time = models.TimeField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        # Update date and time fields to current date and time on every save
        self.date = timezone.now().date()
        self.time = timezone.now().time()
        super().save(*args, **kwargs)
   
    
    
class CourseTable1(models.Model):
    courseid=models.AutoField(primary_key=True)
    weeks=models.CharField(max_length=20,blank=True,default=None)
    text=models.JSONField(default=list,null=True,blank=True)
    heading=models.CharField(max_length=255,default=list)
    video=models.CharField(max_length=128,blank=True)
    PPT=models.CharField(max_length=128,blank=True)
    course_name=models.CharField(max_length=255,default=None,blank=True)

    headings=models.CharField(max_length=255,blank=True)
    
    date = models.DateField(default=timezone.now, blank=True)
    time = models.TimeField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        # Update date and time fields to current date and time on every save
        self.date = timezone.now().date()
        self.time = timezone.now().time()
        super().save(*args, **kwargs)
        
        
        
        
class SurveyTable(models.Model):
    organisation_name=models.CharField(max_length=128)
    start_survey_date=models.DateField(default=timezone.now,blank=True)
    survey_type=models.CharField(max_length=128,blank=True)
    survey_name=models.CharField(max_length=128)
    Max_no_of_participants=models.BigIntegerField(blank=True)
    language=models.CharField(max_length=128)
    survey_questions=models.CharField(max_length=255,blank=True)
    
    def save(self, *args, **kwargs):
       
        self.start_survey_date = timezone.now().date()
        super().save(*args, **kwargs)
    
    
        
        
        
        
class videoTable(models.Model):
    title=models.TextField(max_length=256,null=True)
    video=models.FileField(upload_to='videos/', blank=True,null=True)
    date = models.DateField(default=timezone.now, blank=True)
    time = models.TimeField(default=timezone.now, blank=True)
    
    
    def save(self, *args, **kwargs):
        # Update date and time fields to current date and time on every save
        self.date = timezone.now().date()
        self.time = timezone.now().time()
        super().save(*args, **kwargs)
    

    

class addThoughts(models.Model):
    thought=models.TextField(max_length=256)
    date = models.DateField(default=timezone.now, blank=True)
    time = models.TimeField(default=timezone.now, blank=True)
    
    def save(self, *args, **kwargs):
        # Update date and time fields to current date and time on every save
        self.date = timezone.now().date()
        self.time = timezone.now().time()
        super().save(*args, **kwargs)







    
class allProgramTable(models.Model):
    title=models.TextField(max_length=256,null=True)
    video1=models.FileField(upload_to='videos/', blank=True,null=True)
    PPT1=models.FileField(upload_to='pdf/',blank=True,null=True)
    video2=models.FileField(upload_to='videos/', blank=True,null=True)
    PPT2=models.FileField(upload_to='pdf/',blank=True,null=True)
    video3=models.FileField(upload_to='videos/', blank=True,null=True)
    PPT3=models.FileField(upload_to='pdf/',blank=True,null=True)
    video4=models.FileField(upload_to='videos/', blank=True,null=True)
    PPT4=models.FileField(upload_to='pdf/',blank=True,null=True)
    video5=models.FileField(upload_to='videos/', blank=True,null=True)
    PPT5=models.FileField(upload_to='pdf/',blank=True,null=True)

    date = models.DateField(default=timezone.now, blank=True)
    time = models.TimeField(default=timezone.now, blank=True)
    
    
    def save(self, *args, **kwargs):
        # Update date and time fields to current date and time on every save
        self.date = timezone.now().date()
        self.time = timezone.now().time()
        super().save(*args, **kwargs)