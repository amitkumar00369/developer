# serializers.py
from rest_framework import serializers
from .models1 import AdminTables,CustomUser,OTPVerification_TABLE,AdminTokenTable,UserTokenTable,profile_image_table,Course_table,CourseTable1

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','name','mobile_no', 'email', 'password','profile_image','Designation','date_joined']
        

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
        
        
        
# Motor serializer ---------------------------------------------------------------------------------------------------



        
        
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=profile_image_table
        fields=['profile_image','video_link','ppts']
        
        

        
        
        
        
class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course_table
        fields=['id','weeks','PPT','headings','video','date','time']
        
class CT1Serializer(serializers.ModelSerializer):
    class Meta:
        model=CourseTable1
        fields=['weeks','PPT','headings','video','date','time']
        
