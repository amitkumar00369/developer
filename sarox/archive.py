
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



class archiveCourses(APIView):
    def get(self, request):
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
           
            courses = Course_table.objects.all().order_by('-course_name')
            
            
                
            
            data = {}
            datas=[]
            courseId=[]
            for course in courses:
                if course.active==True:
                    
                    if course.course_id not in courseId:
                        
                    
                        course.archive=True
                        course.save()
                        data= {
                        'course_id': course.course_id,
                        'course_name': course.course_name,
                        'date': course.date
                        }
                        datas.append(data)
                        value=course.archive
                        courseId.append(course.course_id)
                    else:
                        course.archive=True
                        course.save()
                        continue
                        
                    
                    
                else:
                    continue
                
                    
                    
                
                

           
                    # data = {}
                    # seen_course_names = set(cor.course_name for cor in courses)  # Keep track of seen course names
                    # course_list=list(seen_course_names)
                
                
                    # datas=[]
                
            # for cor_name in course_list:
            #     Courses=Course_table.objects.filter(course_name=cor_name).first()
            #     # print('course',Courses)
                   
            #     data= {
            #         'course_id': Courses.course_id,
            #         'course_name': Courses.course_name,
            #         'date': Courses.date
            #         }
            #     datas.append(data)
                        
                   
            return Response({'message':'All archive courses retrieves','data':datas,'archive':value,'status':status.HTTP_200_OK},status.HTTP_200_OK)

  
        except Exception as e:
            return Response({'error':str(e),'status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
