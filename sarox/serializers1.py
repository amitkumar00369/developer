# serializers.py
from rest_framework import serializers
from .models1 import AdminTables,CustomUser,OTPVerification_TABLE,AdminTokenTable,UserTokenTable,profile_image_table,Course_table,CourseTable1
from .models1 import SurveyTable,videoTable,addThoughts,allProgramTable
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','name','mobile_no', 'email', 'password','profile_image','Designation','date_joined','level','No_of_Course','Course_id','Course_name']
        

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

CustomUser._meta.get_field('groups').remote_field.related_name = 'customuser_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'customuser_user_permissions'

        
        


#Admin serializers------


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminTables
        fields = ['email','password']
class AdminStatusChangeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    admin_approval = serializers.BooleanField(default=True)

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserTokenTable
        fields=['user_id','token_store','email']
class AdminTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdminTokenTable
        fields=['user_id','token_store','email']
    
    

        
        


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        models=OTPVerification_TABLE
        fields = ['email', 'otp']
        
        
        




        
        
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=profile_image_table
        fields=['profile_image','video_link','ppts']
        
        

        
        
        
        
class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course_table
        fields=['id','weeks','PPT','headings','headings1','headings2','video','date','time','course_name','course_id','active','archive','start_date','end_date','week_date']
        
class CT1Serializer(serializers.ModelSerializer):
    class Meta:
        model=CourseTable1
        fields=['weeks','PPT','headings','course_name','course_id','video','date','time']
        
        

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model=SurveyTable
        fields=['id','organisation_name','survey_type','start_survey_date','survey_name','Max_no_of_participants','language','survey_questions','pdf_link','submission_count','status']
        
        
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model=videoTable
        fields=['id','title','video','date','time']
        
class thoughSerializer(serializers.ModelSerializer):
    class Meta:
        model=addThoughts
        fields=['id','thought','date','time']
        
        
        
class allProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model=allProgramTable
        fields=['id','title','video1','video2','video3','video4','video5','PPT1','PPT2','PPT3','PPT4','PPT5','date','time']
        
class FeedbackFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    mobile = serializers.CharField(max_length=15)
    feedback = serializers.CharField()