from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models1 import CustomUser,AdminTables,UserTokenTable,AdminStatusTable,AdminTokenTable,OTPVerification_TABLE,profile_image_table,Course_table,CourseTable1
from rest_framework.decorators import api_view
from .serializers1 import UserSerializer,AdminSerializer,UserTokenSerializer,AdminStatusChangeSerializer,AdminTokenSerializer,ImageSerializer,ProgramSerializer,CT1Serializer
from rest_framework.permissions import IsAuthenticated
import jwt,datetime
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect 
import json
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import send_mail
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import EmailMessage
from PIL import Image
# from datetime import datetime


class UserSignIN(APIView):
    def post(self,request):
        try:
            serializer=UserSerializer(data=request.data)
            
            if serializer.is_valid():
                user=serializer.save()
                google_form_link = "https://docs.google.com/forms/d/e/1FAIpQLSf3tbsAaZZfTNU_4mGGOL9l-Hd0U7rXeUPW1PwI1kPfB65vFw/viewform"
                password_change_link = "https://docs.google.com/forms/d/e/1FAIpQLSf3tbsAaZZfTNU_4mGGOL9l-Hd0U7rXeUPW1PwI1kPfB65vFw/viewform"
                portal_login_link = "https://docs.google.com/forms/d/e/1FAIpQLSf3tbsAaZZfTNU_4mGGOL9l-Hd0U7rXeUPW1PwI1kPfB65vFw/viewform"
                email=EmailMessage(
                'Welcome Aboard as a Coach!',
                
                f"""
                Dear {user.name},
                Your email {user.email} and 
                password {user.password},
                
                We're thrilled to welcome you aboard 
                as a coach here at Pro Growth! Your 
                expertise and passionwill undoubtedly 
                enrich the learning journey of our
                clients.
                 
                As a coach, you play a pivotal role in 
                guiding and an inspiring our clients, and
                we're confident that your unique insights
                and experiences will make a significant
                impact.
                
                Here are a few things to get you started:
                To Log in to your coach dashboard,
                Clink the link below to change password.
                ({password_change_link}),
                
                --**Here is the link to the portal,enter your
                email and password to log In.
                ({portal_login_link}),
                
                From here, you can manage your Programs,put
                updates, and access resources to enhance your
                coaching experience.
                
                Familiarize yourself with our coaching guidelines
                and resources available in the coach portal. We're
                continuously updating our materials to ensure you
                have everything you need to succeed.

                We're thrilled to have you join our team and look
                forward to the positive impact you'll make.

                If you have any questions or need assistance, please
                don't hesitate to reach out.

                Welcome aboard, {user.name}!

                Best regards,
                Team,
                PRO GROWTH,
                """,
                
         
                'email@progrowth.coach',  # Replace with your sender email address
                [user.email],  # Extract the email address from the user instance
                # fail_silently=False,
                )
                email.attach_file('unnamed.png')
                email.attach_file('boy1.jpg')
                
                email.send()
                
                return Response({'message':'Coach created successfully','data':serializer.data,'status':status.HTTP_200_OK},status.HTTP_200_OK)
            
            else:
                return Response({'error':serializer.errors},status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'error':str(e)},status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class UserLogIn(APIView):
    def post(self,request):
        try:
            email=request.data.get('email')
            password=request.data.get('password')
            
            if not email:
                return Response({'error':'Invalid Email','status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            user=CustomUser.objects.filter(email=email).first()
            
            if not user:
                return Response({'error':'Coach not found','status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            if password!=user.password:
                return Response({"error": "Password entered is wrong, please check and try again",'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            
            if user:
               
            
            
                if password==user.password:
                    payload = {
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=9),
                    'iat': datetime.datetime.utcnow()
                        }

                    token = jwt.encode(payload=payload, key='secret', algorithm='HS256')
                
                
                    token_table_instance = UserTokenTable.objects.filter(user_id=user.id).first()

          # If an existing token entry exists, update the token, else create a new entry
                    if token_table_instance:
                        token_table_instance.token_store = token
                        token_table_instance.save()
                    else:
                        token_table_instance = UserTokenTable.objects.create(
                        user_id=user.id,
                        token_store=token,
                        email=user.email
                        )
                    return Response({'message':"Coach Login Successfully",'name':user.name,'email':user.email,'image':user.profile_image,'token':token,'status':status.HTTP_200_OK},status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'error':str(e),'status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserLogOut(APIView):
    def post(self, request):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')

        # The token obtained from the header might be prefixed with "Bearer "
        # Remove the "Bearer " prefix if present
        token = token.replace('Bearer ', '')
        

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        userId = payload['id']

        # Retrieve the token instance from the AdminTokenTable
        try:
            token_instance = UserTokenTable.objects.filter(user_id=userId).all()
            token_instance.delete()
            print("Token Deleted Successfully")
        except UserTokenTable.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        return Response({'message': 'Logout successful','status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        
        
        
class UserDetails(APIView):
    def get(self,request,id=None):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')

        # The token obtained from the header might be prefixed with "Bearer "
        # Remove the "Bearer " prefix if present
        token = token.replace('Bearer ', '')
        

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        userId = payload['id']

        # Retrieve the token instance from the AdminTokenTable
        try:
            token_instance = AdminTokenTable.objects.filter(user_id=userId).all()
            tokens=UserTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None and tokens is None:
                return Response({'error':"Token is required",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
      
            if id is None:
                user=CustomUser.objects.all().order_by('-id')
                
                serializer=UserSerializer(user,many=True)
                
                
                return Response({'message':'All Coach details found successfully','data':serializer.data,'status':status.HTTP_200_OK},status.HTTP_200_OK)
                
                
            if id:
                user=CustomUser.objects.filter(id=id).first()
                serializer=UserSerializer(user)
                
            
                return Response({'message':'Coach details found successfully','data':serializer.data,'status':status.HTTP_200_OK},status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'error':'ERROR','data':str(e),'status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
            


class User_profile_update(APIView):
   
    def put(self,request,id=None):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')

        # The token obtained from the header might be prefixed with "Bearer "
        # Remove the "Bearer " prefix if present
        token = token.replace('Bearer ', '')
        

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        userId = payload['id']

        # Retrieve the token instance from the AdminTokenTable
        try:
            token_instance = AdminTokenTable.objects.filter(user_id=userId).all()
            tokens=UserTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None and tokens is None:
                return Response({'error':"Token is required",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
     
     
            if id is None:
               return Response({'error': 'User id not found', 'status': status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
           
    
            user = CustomUser.objects.get(id=id)
           
           
            if user is None:
               return Response({'error': 'Coach not found', 'status': status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)

            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Coach Profile updated successfully', 'data': serializer.data, 'status': status.HTTP_200_OK})
      
           
            else:
                return Response({'error': serializer.errors,'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'Message': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)


           
class forgetPassword(APIView):
    def post(self, request):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')

        # The token obtained from the header might be prefixed with "Bearer "
        # Remove the "Bearer " prefix if present
        token = token.replace('Bearer ', '')
        

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        userId = payload['id']

        # Retrieve the token instance from the AdminTokenTable
        try:
            token_instance = AdminTokenTable.objects.filter(user_id=userId).first()
            tokens=UserTokenTable.objects.filter(user_id=userId).first()
            if token_instance is None and tokens is None:
                return Response({'error':"Token is required",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            data=request.data

            email=data.get('email')
            new_password=data.get('new_password')
            confirm_password=data.get('confirm_password')
            if not email:
                return Response({'error': 'Email is required','status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

            user=CustomUser.objects.filter(email=email).first()
        
            if not user:
                return Response({'error': 'Email not found','status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            if new_password!=confirm_password:
                return Response({'error':'Your password not matched with new password','status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
      
          
        
            if new_password==confirm_password:

                user.password=new_password
                user.save()
                     
                return Response({'message': 'Password changed successfully','status':status.HTTP_200_OK})



   


        except Exception as e:
             print(e)
             return Response({'message': 'Internal server error','status':status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class DeleteCoach(APIView):
    def delete(self,request,id=None):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')

        # The token obtained from the header might be prefixed with "Bearer "
        # Remove the "Bearer " prefix if present
        token = token.replace('Bearer ', '')
        

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        userId = payload['id']

        # Retrieve the token instance from the AdminTokenTable
        try:
            token_instance = AdminTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None:
                return Response({'error':"Token is required",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            if id is None:
                return Response({'error':"Coach id is required",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            coach=CustomUser.objects.filter(id=id).first()
            if coach is None:
                return Response({'error':"Coach not found",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            serializer=UserSerializer(coach,many=True)
            if coach:
                
            
                coach.delete()
               
            
                return Response({'message':'Coach successfully deleted','status':status.HTTP_200_OK},status.HTTP_200_OK)
            
            
        except Exception as e:
            return Response({'error':str(e),'status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
class ResetPassword(APIView):
    def post(self, request):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')

        # The token obtained from the header might be prefixed with "Bearer "
        # Remove the "Bearer " prefix if present
        token = token.replace('Bearer ', '')
        

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        userId = payload['id']

        # Retrieve the token instance from the AdminTokenTable
        try:
            token_instance = UserTokenTable.objects.filter(user_id=userId).first()
            # tokens=AdminTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None:
                return Response({'error':"Coach token not found",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            data=request.data

            email=data.get('email')
            new_password=data.get('new_password')
        # confirm_password=data.get('confirm_password')
            if not email:
                return Response({'error': 'Email is required','status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            if not  new_password:
                return Response({'error': 'Entered New Password','status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

            user=CustomUser.objects.filter(email=email).first()
            if not user:
                return Response({'error': 'Coach not found','status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        # email_in_otp_table=OTPVerification_TABLE.objects.filter(email=email).first()
            if  user.email!=token_instance.email:
                return Response({'error': 'Email not matched with token','status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        # print(email_in_otp_table.email)
        # print(email)
       
            # if email_in_otp_table.email==email:
        

            user.password=new_password
            user.save()
                    # email_in_otp_table.delete()
            return Response({'message': 'Coach changed password successfully','status':status.HTTP_200_OK})

       

      


        except Exception as e:
            print(e)
            return Response({'message': 'Internal server error','status':status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                
            
            
                
         













        
        
#ADMIN code ---------------------------------------------------------------------------------------

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class AdminSignIN(APIView):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        try:
            serializer = AdminSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Admin has been created successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            
            else:
                return Response({'error': serializer.errors}, status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        
class AdminLogIn(APIView):
    def post(self,request):
        try:
            email=request.data.get('email')
            password=request.data.get('password')
            
            if not email:
                return Response({'error':'Invalid Email','status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            user=AdminTables.objects.filter(email=email).first()
            
            if not user:
                return Response({'error':'Admin not found','status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            if not check_password(password,user.password):
                return Response({"error": "Password entered is wrong, please check and try again",'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            
            if user:
                if check_password(password,user.password):
                    payload = {
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=9),
                    'iat': datetime.datetime.utcnow()
                        }

                    token = jwt.encode(payload=payload, key='secret', algorithm='HS256')
                
                
                    token_table_instance = AdminTokenTable.objects.filter(user_id=user.id).first()

          # If an existing token entry exists, update the token, else create a new entry
                    if token_table_instance:
                        token_table_instance.token_store = token
                        token_table_instance.save()
                    else:
                        token_table_instance = AdminTokenTable.objects.create(
                        user_id=user.id,
                        token_store=token,
                        email=user.email
                        )
                    return Response({'message':"Admin Login Successfully",'token':token,'email':user.email,'status':status.HTTP_200_OK},status.HTTP_200_OK)
                
                    
                
        except Exception as e:
            return Response({'error':str(e),'status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class AdminLogOut(APIView):
    def post(self,request):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')

        # The token obtained from the header might be prefixed with "Bearer "
        # Remove the "Bearer " prefix if present
        token = token.replace('Bearer ', '')
        

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        userId = payload['id']

        # Retrieve the token instance from the AdminTokenTable
        try:
            token_instance = AdminTokenTable.objects.filter(user_id=userId).all()
            token_instance.delete()
            print("Token Deleted Successfully")
        except AdminTokenTable.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        return Response({'message': 'Logout successful','status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        


class ChangePassword(APIView):
    def post(self,request):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')

        # The token obtained from the header might be prefixed with "Bearer "
        # Remove the "Bearer " prefix if present
        token = token.replace('Bearer ', '')
        

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        userId = payload['id']

        # Retrieve the token instance from the AdminTokenTable
        try:
            token_instance = AdminTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None:
                return Response({'error':"Admin token not found",'status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
                
        
            email=request.data.get('email')
            new_password=request.data.get('password')
            if email is None:
                return Response({'error':"Please enter email",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            if not new_password:
                return Response({'error':"Please enter new password",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
                
                
            
            admin=AdminTables.objects.filter(id=userId).first()
            if admin is None:
                return Response({'error':"Admin not found",'status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
            if admin.email!=email:
                return Response({'error':"Admin email not matched",'status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
                
            admin.password=new_password
            admin.save()
            return Response({'message':'Admin changed password successfully','status':status.HTTP_200_OK},status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            


# Media section using AWS cloud Storage

class Imageupload(APIView):
    parser_classes = [MultiPartParser, FormParser]
    

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        print(serializer)
      
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Image Upload successfully', 'data': serializer.data})
        
        # Handle case when serializer is not valid
        return Response({'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
# Programe table ---------------------------------------------------------------------

# from datetime import datetime
class WeekProgram(APIView):
    def post(self,request):
        parser_classes = [MultiPartParser, FormParser]
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')

        # The token obtained from the header might be prefixed with "Bearer "
        # Remove the "Bearer " prefix if present
        token = token.replace('Bearer ', '')
        

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        userId = payload['id']

        # Retrieve the token instance from the AdminTokenTable
        try:
            token_instance = AdminTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None:
                return Response({'error':"Token is required",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            from datetime import datetime
            course_name=request.data.get('course_name')
            subheading=request.data.get('text')
            heading=request.data.get('heading')
            subheading1=request.data.get('text1')
            heading1=request.data.get('heading1')
            subheading2=request.data.get('text2')
            heading2=request.data.get('heading2')
            weeks=request.data.get('weeks')
            # date_str= request.data.get('date')
            # if not date_str:
            #     return Response({'error':"date not found",'status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
            # assigned_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            # formatted_date = assigned_date.strftime("%Y-%m-%d")
            
            programs = Course_table.objects.all()
            course_names_set = {pro.course_name for pro in programs}
            
            serializer=ProgramSerializer(data=request.data,partial=True)
            if serializer.is_valid():
                prog = serializer.save()
                
                 # Assuming course_name is defined elsewhere

  
                prog.course_name = course_name
                headings_dict = {"heading": [heading], "subheading": subheading}
                headings_dict1 = {"heading": [heading1], "subheading": subheading1}
                headings_dict2 = {"heading": [heading2], "subheading": subheading2}
                json_string = json.dumps(headings_dict)
                json_string1 = json.dumps(headings_dict1)
                json_string2 = json.dumps(headings_dict2)
                prog.headings = json_string
                prog.headings1 = json_string1
                prog.headings2 = json_string2
                prog.course_id=prog.course_id
                prog.weeks=weeks
                
                prog.save()


                

    
                
                
                course_ids_set = [pro.course_id for pro in programs]
                print('program',course_names_set)
                
                if prog.course_name:
                    couser=Course_table.objects.filter(course_name=prog.course_name).first()
                    
                    if course_name in course_names_set:
                        
                
                         prog.course_id = couser.course_id
                         prog.date=couser.date
                         prog.save()
                    

    
                    if course_name not in course_names_set:
 
                        prog.course_id = max(course_ids_set)+1
                        prog.date=datetime.today().date()
                        # prog.coure_id=1
                        prog.save()
                elif prog.course_name not in course_names_set:
      
                    return Response({'error': 'Course name does not match any existing courses.', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    
    
               

 
                return Response({
        'message': 'Program submitted successfully',
        'course_name': course_name,
        'course_id': prog.course_id,
        'data':{'week':prog.weeks,'details':serializer.data},
        'status': status.HTTP_200_OK
        
        }, status=status.HTTP_200_OK)

            
            

            
            else:
                return Response({'error':serializer.errors,'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
                
            

        except AdminTokenTable.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        
    
    
    
    
# get all data when week 

class ByCourseName(APIView):
    def get(self, request, cid=None):
        
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')

        # The token obtained from the header might be prefixed with "Bearer "
        # Remove the "Bearer " prefix if present
        token = token.replace('Bearer ', '')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        userId = payload['id']

        # Retrieve the token instance from the AdminTokenTable
        try:
            token_instance = UserTokenTable.objects.filter(user_id=userId).first()
            tokens = AdminTokenTable.objects.filter(user_id=userId).first()
            if token_instance is None and tokens is None:
                return Response({'error': "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

            user = CustomUser.objects.filter(id=userId).first()
            if user is None:
                return Response({'error': "User not found"}, status=status.HTTP_400_BAD_REQUEST)

            if cid is None:
                program = Course_table.objects.all().order_by('-id')
                course_name=set(cor.course_name for cor in program)
                course_id=set(cor.course_id for cor in program)
                
            else:
                program = Course_table.objects.filter(course_id=cid).all()
                program = Course_table.objects.filter(course_id=cid).all()
                course_details = []
                if not program:
                    return Response({'message':'Course not found','status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)

# Dictionary to store details by week name
                week_details = {}

                for prog in program:
                    if prog is None:
                        continue
    
    # Check if week_name already exists in week_details
                    if prog.weeks in week_details:
                            week_details[prog.weeks].append({
                                    'id': prog.id,
                                    'PPT': prog.PPT.url if prog.PPT and hasattr(prog.PPT, 'url') else None,
                                    'headings': prog.headings,
                                    'video': prog.video.url if prog.video and hasattr(prog.video, 'url') else None,
                                    'date': prog.date,
                                    'active':prog.active
                                    })
                    else:
                        week_details[prog.weeks] = [{
                        'id': prog.id,
                        'PPT': prog.PPT.url if prog.PPT and hasattr(prog.PPT, 'url') else None,
                        'headings': prog.headings,
                        'video': prog.video.url if prog.video and hasattr(prog.video, 'url') else None,
                        'date': prog.date,
                        'active':prog.active
                        
                        }]

# Convert week_details into the required format
            for week, details_list in week_details.items():
                week_details_dict = {'week_name': week,'week_date':{prog.week_date for prog in program if prog.weeks==week if prog.week_date} or None}
                for index, details in enumerate(details_list, start=1):
                    week_details_dict['details{}'.format(index)] = details
                course_details.append(week_details_dict)

# Now course_details contains the restructured data

                # course_details=[]
                
                # for prog in program:
                #     if prog is None:
                #         continue
                        
                    
                #     course_details.append({'week_name':prog.weeks,
                #         'details':{"id": prog.id,  
                #          "PPT": prog.PPT.url if prog.PPT and hasattr(prog.PPT, 'url') else None,
                #          "headings": prog.headings,
                #         #  "headings1":  prog.headings1,
                #         #  "headings2": prog.headings2,
                #          "video": prog.video.url if prog.video and hasattr(prog.video, 'url') else None,
                #         "date": prog.date
                #     },     
                                                           
                #     })
                    # course_details.append()
                    
                    
                    
                course_name=set(cor.course_name for cor in program)
                course_id=set(cor.course_id for cor in program)
                bool_value=set(cor.active for cor in program)
                count=len(bool_value)
                if count==1:
                    if False in bool_value:
                        for course in program:
                            course.archive=False
                            value=course.archive=False
                            course.save()
                        
                        
                    else:
                        for course in program:
                            course.archive=True
                            value=course.archive=True
                            course.save()
                       
                else:
                    for course in program:
                        course.archive=False
                        value=course.archive=False
                        course.save()

                
                # heading=[prog.heading for prog in program]
                # weeks_name = [prog.weeks for prog in program]
                # heading=[prog.heading for prog in program]
                # heading=[prog.heading for prog in program]
                

            serializer = ProgramSerializer(program, many=True) 
        
            # Pass data to serializer
            return Response({'message': 'Get all programs', 'course_name':course_name,'course_id':course_id,'details':course_details,'archive':value}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
           


class CourseName(APIView):
    def get(self, request, cid=None):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')

        # The token obtained from the header might be prefixed with "Bearer "
        # Remove the "Bearer " prefix if present
        token = token.replace('Bearer ', '')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        userId = payload['id']

        # Retrieve the token instance from the AdminTokenTable
        try:
            token_instance = UserTokenTable.objects.filter(user_id=userId).first()
            tokens=AdminTokenTable.objects.filter(user_id=userId).first()
   
            if token_instance is None and tokens is None:
                return Response({'error': "Token is required"}, status=status.HTTP_400_BAD_REQUEST)
            if cid is None:

                courses = Course_table.objects.all().order_by('-course_name')
                

           
            data = {}
            seen_course_names = set(cor.course_name for cor in courses)  # Keep track of seen course names
            course_list=list(seen_course_names)
                
                
            datas=[]
                
            for cor_name in course_list:
                Courses=Course_table.objects.filter(course_name=cor_name).first()
                # print('course',Courses)
                   
                data= {
                    'course_id': Courses.course_id,
                    'course_name': Courses.course_name,
                    'date': Courses.date,
                    # 'week_date':courses.week_date,
                    }
                datas.append(data)
                        
                   
            return Response({'message':'All courses retrieves','data':datas,'courses_name':course_list,'No_of_courses':len(course_list),'status':status.HTTP_200_OK},status.HTTP_200_OK)

  
        except Exception as e:
            return Response({'error':str(e),'status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class deleteCourse(APIView):
    def delete(self,request,cid=None):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')

        # The token obtained from the header might be prefixed with "Bearer "
        # Remove the "Bearer " prefix if present
        token = token.replace('Bearer ', '')
        

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        userId = payload['id']

        # Retrieve the token instance from the AdminTokenTable
        try:
            token_instance = UserTokenTable.objects.filter(user_id=userId).all()
            tokens=AdminTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None and tokens is None:
                return Response({'error':"Token not found",'status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
            if cid is None:
                return Response({'error':"Course Id  is required",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            course=Course_table.objects.filter(course_id=cid).all()
            if not course:
                return Response({'error':"Course not found",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            serializer=ProgramSerializer(course,many=True)
            course.delete()
          
            if serializer:
               
                return Response({'message':'Course deleted successfully','data':serializer.data,'status':status.HTTP_200_OK},status.HTTP_200_OK)
            
            else:
                return Response({'error':serializer.errors},status=400)
            
            
        except Exception as e:
            return Response({'error':str(e)},status=500)


            
        

   
    
    

        


class CourseTable1Reg(APIView):
    def post(self, request):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')

        # The token obtained from the header might be prefixed with "Bearer "
        # Remove the "Bearer " prefix if present
        token = token.replace('Bearer ', '')
        

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        userId = payload['id']

        # Retrieve the token instance from the AdminTokenTable
        try:
            token_instance = AdminTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None:
                return Response({'error':"Token is required",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
        
            course_name=request.data.get('course_name')
            text=request.data.get('text')
            heading=request.data.get('heading')
            serializer=CT1Serializer(data=request.data)
            
            if serializer.is_valid():
                prog=serializer.save()
                prog.course_name=course_name
                prog.headings={'heading':[heading],'subheading':text}
                
                prog.save()
                return Response({'message':'Program submitted successfully','data':serializer.data,'course_id':prog.courseid,'course_name':course_name,'status':status.HTTP_200_OK},status.HTTP_200_OK)
            
            else:
                return Response({'error':serializer.errors,'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
        except AdminTokenTable.DoesNotExist:
            return Response({'error':'Token not found','statsu':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error':str(e),'status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        


class GetAllCourse(APIView):
    def get(self,request,id=None):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')

        # The token obtained from the header might be prefixed with "Bearer "
        # Remove the "Bearer " prefix if present
        token = token.replace('Bearer ', '')
        

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        userId = payload['id']

        # Retrieve the token instance from the AdminTokenTable
        try:
            token_instance = AdminTokenTable.objects.filter(user_id=userId).all()
            
            if token_instance is None:
                return Response({'error':"Token is required",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            
            if id is None:
                course=CourseTable1.objects.all()
                data = {}
                for index, course in enumerate(course, start=0):
                    data[index] = {
                   
                    'course_id': course.courseid,
                    'course_name': course.course_name,
                    'date':course.date
                    }
            
                return Response(data, status=200)
            if id:
                course=CourseTable1.objects.filter(courseid=id).first()
                
                return Response({'message':'Successfull','course_name':course.course_name,'course_id':course.courseid},status=200)
            else:
                return Response({'error': 'Not defined'}, status=400)
                
        except Exception as e:
            return Response({'error':str(e),'status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
                
class UpdateInCT1(APIView):
    def put(self,request,id=None):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')

        # The token obtained from the header might be prefixed with "Bearer "
        # Remove the "Bearer " prefix if present
        token = token.replace('Bearer ', '')
        

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        userId = payload['id']

        # Retrieve the token instance from the AdminTokenTable
        try:
            token_instance = AdminTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None:
                return Response({'error':"Token is required",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            
            if id is None:
                return Response({'error': 'Not defined'}, status=400)
              
            if id:
                course_name=request.data.get('course_name')
                course=CourseTable1.objects.filter(courseid=id).first()
                if not course:
                    return Response({'error': 'Not defined'}, status=400)
                    
                serializer=CT1Serializer(course,data=request.data,partial=True)
                if serializer.is_valid():
                    c=serializer.save()
                    c.course_name=course_name
                    c.save()
                    
                
                    return Response({'message':'Successfull','data':serializer.data,'course_id':course.courseid,'course_name':course.course_name},status=200)
            else:
                return Response({'error': 'Not defined'}, status=400)
                
        except Exception as e:
            return Response({'error':str(e),'status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
class GetAllCourseByUser(APIView):
    def get(self,request,id=None):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')

        # The token obtained from the header might be prefixed with "Bearer "
        # Remove the "Bearer " prefix if present
        token = token.replace('Bearer ', '')
        

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        userId = payload['id']

        # Retrieve the token instance from the AdminTokenTable
        try:
            token_instance = UserTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None:
                return Response({'error':"Token is required",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            
            if id is None:
                course=CourseTable1.objects.all()
                data = {}
                for index, course in enumerate(course, start=0):
                    data[index] = {
                   
                    'course_id': course.courseid,
                    'course_name': course.course_name,
                    'date':course.date
                    }
            
                return Response(data, status=200)
            if id:
                course=CourseTable1.objects.filter(courseid=id).first()
                
                return Response({'message':'Successfull','course_name':course.course_name,'course_id':course.courseid},status=200)
            else:
                return Response({'error': 'Not defined'}, status=400)
                
        except Exception as e:
            return Response({'error':str(e),'status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
class ByCourseID(APIView):
    def get(self, request, id=None):
        
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')

        # The token obtained from the header might be prefixed with "Bearer "
        # Remove the "Bearer " prefix if present
        token = token.replace('Bearer ', '')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        userId = payload['id']

        # Retrieve the token instance from the AdminTokenTable
        try:
            token_instance = UserTokenTable.objects.filter(user_id=userId).first()
            if token_instance is None:
                return Response({'error': "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

            user = CustomUser.objects.filter(id=userId).first()
            if user is None:
                return Response({'error': "User not found"}, status=status.HTTP_400_BAD_REQUEST)

            if id is None:
                return Response({'error': "course id not found"}, status=status.HTTP_400_BAD_REQUEST)
             
                
            if id:
                course=CourseTable1.objects.filter(courseid=id).first()
                print('course',course)
                
            
                serializer = CT1Serializer(course)
                if serializer:
                    
                    return Response({'message': 'Get all programs', 'data': {'details':serializer.data,'course_name':course.course_name,'course_id':course.courseid}}, status=status.HTTP_200_OK) 
                
                else:
                    return Response({'error':'Not defined'},status=400)
                        
 

    

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)