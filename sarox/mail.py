from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models1 import CustomUser,AdminTables,UserTokenTable,AdminStatusTable,AdminTokenTable,OTPVerification_TABLE,profile_image_table,Course_table,CourseTable1,videoTable
from rest_framework.decorators import api_view
from .serializers1 import UserSerializer,AdminSerializer,UserTokenSerializer,AdminStatusChangeSerializer,AdminTokenSerializer,ImageSerializer,ProgramSerializer,CT1Serializer,VideoSerializer
from rest_framework.permissions import IsAuthenticated
import jwt,datetime
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect 
import json
from django.core.mail import send_mail
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import EmailMessage
from PIL import Image
from django.http import JsonResponse
from .models1 import addThoughts
from .serializers1 import thoughSerializer
class sendMail(APIView):
    
    def post(self, request):
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
            token_instance = UserTokenTable.objects.filter(user_id=userId).all()
            tokens=AdminTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None and tokens is None:
                return Response({'error':"Token not found",'status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
     
       
            user = CustomUser.objects.filter(id=userId).first()
         
            if not user:
                return Response({'error': 'Email not found','status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            google_form_link = "https://docs.google.com/forms/d/e/1FAIpQLSf3tbsAaZZfTNU_4mGGOL9l-Hd0U7rXeUPW1PwI1kPfB65vFw/viewform"

            email=EmailMessage(
                'This mail recieved from vijay johar bussiness pvt Ltd.',
                f'Please fill the form:- {google_form_link}',
                'amitraazec53@gmail.com',  # Replace with your sender email address
                [user.email],  # Extract the email address from the user instance
                # fail_silently=False,
            )
            email.attach_file('unnamed.png')
            email.attach_file('boy1.jpg')
            email.attach_file('Techahead_resume.pdf')    
            email.send()
            return Response({'message': 'message sent successfully', 'email':user.email,'status': status.HTTP_200_OK})

        except Exception as e:
            return Response({'error': 'Internal server error','message':str(e), 'status': status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)



class videoUpload(APIView):
    def post(self, request):
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
            token_instance = UserTokenTable.objects.filter(user_id=userId).all()
            tokens=AdminTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None and tokens is None:
                return Response({'error':"Token not found",'status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)

            serializer = VideoSerializer(data=request.data)
        
      
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Video Upload successfully', 'data': serializer.data,'status':status.HTTP_200_OK},status=200)
            else:
                return Response({'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':str(e)},status=500)
        
        
        
class getAllVideo(APIView):
    def get(self, request,id=None):
        # parser_classes = [MultiPartParser, FormParser]
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
            
            
            if not id:
                videos=videoTable.objects.all().order_by('-id')
                
                serializer=VideoSerializer(videos,many=True)
            elif id:
                videos=videoTable.objects.filter(id=id).first()
                
                serializer=VideoSerializer(videos)
                
            if serializer:
          
                return Response({'message': 'get video succussfully','data': serializer.data,'status':status.HTTP_200_OK},status=200)
            else:
                return Response({'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':str(e)},status=500)
class deleteVideo(APIView):
    def delete(self, request,id=None):
        # parser_classes = [MultiPartParser, FormParser]
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')
        if not id:
            return Response({'error':"Please enter post ID",'status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)

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

            
            videos=videoTable.objects.filter(id=id).first()
          
            if videos is None:
                return Response({'error':"videos not exist",'status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
                
         
            serializer=VideoSerializer(videos)
            videos.delete()
           
            if serializer:
                
          
                return Response({'message': 'deleted succussfully','status':status.HTTP_200_OK},status=200)
            else:
                return Response({'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':str(e)},status=500)
        
        
        
class updateVideo(APIView):
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
            token_instance = UserTokenTable.objects.filter(user_id=userId).all()
            tokens=AdminTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None and tokens is None:
                return Response({'error':"Token not found",'status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
            if id is None:
                return Response({'error':"Id  is required",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            video=videoTable.objects.filter(id=id).first()
            if not video:
                return Response({'error':"video not found",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            serializer=VideoSerializer(video,data=request.data,partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Video updated successfully','data':serializer.data,'status':status.HTTP_200_OK},status.HTTP_200_OK)
            
            else:
                return Response({'error':serializer.errors},status=400)
            
            
        except Exception as e:
            return Response({'error':str(e)},status=500)

        
        
        
        
        
        
class postThought(APIView):
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
            tokens=AdminTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None and tokens is None:
                return Response({'error':"Token not found",'status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)

            serializer = thoughSerializer(data=request.data)
        
      
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Your thoughts posted successfully', 'data': serializer.data,'status':status.HTTP_200_OK},status=200)
            else:
                return Response({'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':str(e)},status=500)
        
        
class getAllThoughts(APIView):
    def get(self, request,id=None):
        # parser_classes = [MultiPartParser, FormParser]
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
            if not id:
                thought=addThoughts.objects.all().order_by('-id')
                serializer=thoughSerializer(thought,many=True)
            elif id:
                thought=addThoughts.objects.filter(id=id).first()
                serializer=thoughSerializer(thought)
            if serializer:
          
                return Response({'message': 'get thoughts succussfully','data': serializer.data,'status':status.HTTP_200_OK},status=200)
            else:
                return Response({'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':str(e)},status=500)
  
class deleteThoughts(APIView):
    def delete(self, request,id=None):
        # parser_classes = [MultiPartParser, FormParser]
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')
        if not id:
            return Response({'error':"Please enter post ID",'status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)

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

            
            thought=addThoughts.objects.filter(id=id).first()
          
            if thought is None:
                return Response({'error':"postId not exist",'status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
                
         
            serializer=thoughSerializer(thought)
            thought.delete()
           
            if serializer:
                
          
                return Response({'message': 'deleted succussfully','status':status.HTTP_200_OK},status=200)
            else:
                return Response({'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':str(e)},status=500)
  
  
  
  