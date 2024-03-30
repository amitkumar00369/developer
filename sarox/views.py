from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models1 import CustomUser,AdminTables,UserTokenTable,AdminStatusTable,AdminTokenTable,OTPVerification_TABLE,profile_image_table
from rest_framework.decorators import api_view
from .serializers1 import UserSerializer,AdminSerializer,UserTokenSerializer,AdminStatusChangeSerializer,AdminTokenSerializer,ImageSerializer
from rest_framework.permissions import IsAuthenticated
import jwt,datetime
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect 
import json


class UserSignIN(APIView):
    def post(self,request):
        try:
            serializer=UserSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                
                return Response({'message':'User has been created successfully','data':serializer.data,'status':status.HTTP_200_OK},status.HTTP_200_OK)
            
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
                return Response({'error':'User not found','status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
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
                    return Response({'message':"User Login Successfully",'token':token,'status':status.HTTP_200_OK},status.HTTP_200_OK)
                
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
        try:
            if id is None:
                user=CustomUser.objects.all().order_by('-id')
                
                serializer=UserSerializer(user,many=True)
                
                
                return Response({'message':'All user details found successfully','data':serializer.data,'status':status.HTTP_200_OK},status.HTTP_200_OK)
                
                
            if id:
                user=CustomUser.objects.filter(id=id).first()
                serializer=UserSerializer(user)
                
            
                return Response({'message':'User details found successfully','data':serializer.data,'status':status.HTTP_200_OK},status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'error':'ERROR','data':str(e),'status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
            


class User_profile_update(APIView):
   
    def put(self,request,id=None):
        try:
     
           if id is None:
               return Response({'error': 'User id not found', 'status': status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
           
    
           user = CustomUser.objects.get(id=id)
           
           
           if user is None:
               return Response({'error': 'User not found', 'status': status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)

           serializer = UserSerializer(user, data=request.data, partial=True)
           if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User Profile updated successfully', 'data': serializer.data, 'status': status.HTTP_200_OK})
      
           
           else:
                return Response({'error': serializer.errors,'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            
            return Response({'Message': 'Internal Server Error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)


           
        
        
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
                return Response({'message': 'User has been created successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            
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
                return Response({'error':'User not found','status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            if not check_password(password,user.password):
                return Response({"error": "Password entered is wrong, please check and try again",'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            
            if user:
                if check_password(password,user.password):
                    return Response({'message':"Admin Login Successfully",'status':status.HTTP_200_OK},status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'error':str(e),'status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class AdminLogOut(APIView):
    def post(self,request):
        try:
            email=request.data.get('email')
            
            if not email:
                return Response({'error':'Please Enter Valid Email','status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            
            user=AdminTables.objects.filter(email=email).first()
            
            if not user:
                return Response({'error':'Admin not found','status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            if user:
                return Response({'message':'Admin Logout Successfull','status':status.HTTP_200_OK},status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error':str(e),'status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
            







# Media section using AWS cloud Storage

from rest_framework.parsers import MultiPartParser, FormParser
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