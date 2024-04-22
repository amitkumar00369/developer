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
from .models1 import addThoughts,allProgramTable
from .serializers1 import thoughSerializer,allProgramSerializer



class CreateallProgram(APIView):
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
            tokens=UserTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None and tokens is None:
                return Response({'error':"Token is required",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            serializer=allProgramSerializer(data=request.data,partial=True)
            
            if serializer.is_valid():
                program=serializer.save()


                
                return Response({'message':'programs created successfully','data':serializer.data,
                                'status':status.HTTP_200_OK},status.HTTP_200_OK)
            
            else:
                return Response({'message':serializer.errors,'status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({'error':str(e),'status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class getAllProgram(APIView):
    def get(self, request, pid=None):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')

        token = token.replace('Bearer ', '')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        userId = payload['id']

        try:
            token_instance = UserTokenTable.objects.filter(user_id=userId).all()
            tokens = AdminTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None and tokens is None:
                return Response({'error': "Token not found", 'status': status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

            if not pid:
                programs = allProgramTable.objects.all()

                response_data = []
                for program in programs:
                    
          
                    if program:
                        program_data = {}
                        program_data1={} 
                        for i in range(1, 6):
                            ppt_key = f'PPT{i}'
                            ppt_value = getattr(program, ppt_key)
                            if ppt_value:
                                if hasattr(ppt_value, 'url'):
                                    ppt_url = ppt_value.url  # Assuming it's a URLField
                                    program_data[ppt_key] = ppt_url
                                elif hasattr(ppt_value, 'path'):
                                    ppt_path = ppt_value.path  # Assuming it's a FilePathField
                                    program_data[ppt_key] = ppt_path
                                else:
                                    program_data[ppt_key] = None
                            else:
                                program_data[ppt_key] = None
                        for i in range(1, 6):
                            ppt_key = f'video{i}'
                            ppt_value = getattr(program, ppt_key)
                            if ppt_value:
                                if hasattr(ppt_value, 'url'):
                                    ppt_url = ppt_value.url  # Assuming it's a URLField
                                    program_data1[ppt_key] = ppt_url
                                elif hasattr(ppt_value, 'path'):
                                    ppt_path = ppt_value.path  # Assuming it's a FilePathField
                                    program_data1[ppt_key] = ppt_path
                                else:
                                    program_data1[ppt_key] = None
                            else:
                                program_data1[ppt_key] = None
                        data ={
                        'id': program.id,
                        'video': program_data1,
                        'ppt': program_data
                    
                        }
                       
                        response_data.append(data)
                        
                    else:
                        pass
                return Response({'message': 'get programs successfully', 'data':response_data, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
         
                
                    
                
        

                       
                    
                # serializer = allProgramSerializer(programs, many=True)
                # return Response({'message': 'get programs successfully', 'data': serializer.data,'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
            elif pid:
                program = allProgramTable.objects.filter(id=pid).first()
                if not program:
                    return Response({'message': 'Program not found','status':status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
                    
                program_data = {}
                
                for i in range(1, 6):
                    ppt_key = f'PPT{i}'
                    
                    ppt_value = getattr(program, ppt_key)
       
                    if ppt_value:
                        if hasattr(ppt_value, 'url'):
                            ppt_url = ppt_value.url  # Assuming it's a URLField
                            program_data[ppt_key] = ppt_url
                        elif hasattr(ppt_value, 'path'):
                            ppt_path = ppt_value.path  # Assuming it's a FilePathField
                            program_data[ppt_key] = ppt_path
                        else:
                            program_data[ppt_key] = None
                    else:
                        program_data[ppt_key] = None
                program_data1={}      
                for i in range(1, 6):
                    ppt_key = f'video{i}'
                    
                    ppt_value = getattr(program, ppt_key)
        
                    if ppt_value:
                        if hasattr(ppt_value, 'url'):
                            ppt_url = ppt_value.url  # Assuming it's a URLField
                            program_data1[ppt_key] = ppt_url
                        elif hasattr(ppt_value, 'path'):
                            ppt_path = ppt_value.path  # Assuming it's a FilePathField
                            program_data1[ppt_key] = ppt_path
                        else:
                            program_data1[ppt_key] = None
                    else:
                        program_data1[ppt_key] = None

                return Response({'message': 'get program successfully','id':program.id, 'video': program_data1,'ppts':program_data, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

         
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class deleteProgram(APIView):
    def delete(self, request,pid=None):
        # parser_classes = [MultiPartParser, FormParser]
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token is required for this operation')
        if not pid:
            return Response({'error':"Please enter  ID",'status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)

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

            
            program=allProgramTable.objects.filter(id=pid).first()
          
            if program is None:
                return Response({'error':"programs not exist",'status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
                
         
            serializer=allProgramSerializer(program)
            program.delete()
           
            if serializer:
                
          
                return Response({'message': 'deleted succussfully','status':status.HTTP_200_OK},status=200)
            else:
                return Response({'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':str(e)},status=500)
        
        
        
class updateProgram(APIView):
    def put(self,request,pid=None):
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
            if pid is None:
                return Response({'error':"Id  is required",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            program=allProgramTable.objects.filter(id=pid).first()
            if not program:
                return Response({'error':"program not found",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            serializer=allProgramSerializer(program,data=request.data,partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Program updated successfully','data':serializer.data,'status':status.HTTP_200_OK},status.HTTP_200_OK)
            
            else:
                return Response({'error':serializer.errors},status=400)
            
            
        except Exception as e:
            return Response({'error':str(e)},status=500)

