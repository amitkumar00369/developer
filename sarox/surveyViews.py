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
from .models1 import SurveyTable
from .serializers1 import SurveySerializer
from django.conf import settings
import os
import io
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from .models import QuestionAnswer,PostQuestionAnswer,PreQuestionAnswer
from reportlab.lib.pagesizes import A4,A0
import boto3




class CreateSurvey(APIView):
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
            tokens=UserTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None and tokens is None:
                return Response({'error':"Token is required",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            
            serializer=SurveySerializer(data=request.data)
            
            
            if serializer.is_valid():
                survey=serializer.save()
                
                
#---------------------------------------------PRE----------------------------------------------------------
                if survey.survey_type=="PRE":

                    # pdf_filename = f"PreSurveydata_{survey.id}.pdf"
                    # pdf_filepath = os.path.join(settings.MEDIA_ROOT, pdf_filename)
                    pdf_buffer = io.BytesIO()


                    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)

 
                    data = PreQuestionAnswer.objects.all().order_by('suggestion')
 

                    grouped_data = {}
                    for entry in data:
                        if entry.suggestion not in grouped_data:
                            grouped_data[entry.suggestion] = {
                            "questions": [],
                            "answers": []
                            }
                        grouped_data[entry.suggestion]["questions"].append(entry.question)
       
                        grouped_data[entry.suggestion]["answers"].append(entry.answer)


                    table_data = [["Suggestions1","Questions", "Answers"]]  # Header row
                    styles = getSampleStyleSheet()
    
                    for suggestion, details in grouped_data.items():
                        questions = "<br/>".join([f"{i+1}. {q}" for i, q in enumerate(details["questions"])])

                        answers = "<br/>".join([f"{i+1}. {a}" for i, a in enumerate(details["answers"])])

                        table_data.append([
                        suggestion,
                        Paragraph(questions, styles['Normal']),

                        Paragraph(answers, styles['Normal']),
       
                       ])
     
                    table = Table(table_data, colWidths=[150,250,100])
                    table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ]))

    
                    doc.build([table])
                    pdf_buffer.seek(0)
                    s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_S3_REGION_NAME)
                    folder_path = f"PreSurvey/"  # Define the folder path
                    file_key = f"{folder_path}PreSurveydata_{survey.id}.pdf" 
                    s3.upload_fileobj(pdf_buffer, settings.AWS_STORAGE_BUCKET_NAME,file_key, ExtraArgs={'ContentType': 'application/pdf'})

    # Construct the PDF URL
                    pdf_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_key}"

    # Save the PDF link in the survey object
                    survey.pdf_link = pdf_url
                    # s3 = boto3.client('s3',
                    #   aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    #   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    #   region_name=settings.AWS_S3_REGION_NAME)

                    # with open(pdf_filepath, 'rb') as pdf_file:
                    #     s3.upload_fileobj(pdf_file, settings.AWS_STORAGE_BUCKET_NAME, pdf_filename)

   
                    # pdf_url = f"{settings.MEDIA_URL}{pdf_filename}"

   
                    # survey.pdf_link = pdf_url
                    survey.submission_count=len(list(set(post.suggestion for post in data)))
                    survey.save()
                    data.delete()


 

    #-------------------------------------------------------------------------------------------------------------------POST--------------------------
                
                if survey.survey_type=="POST":
                    # pdf_filename = f"PostSurveydata_{survey.id}.pdf"
                    # pdf_filepath = os.path.join(settings.MEDIA_ROOT, pdf_filename)
                    pdf_buffer = io.BytesIO()
                    
                    doc = SimpleDocTemplate(pdf_buffer, pagesize=A0)

 
                    data = PostQuestionAnswer.objects.all().order_by('email')

   
                    grouped_data = {}
                    for entry in data:
                        if entry.email not in grouped_data:
                            grouped_data[entry.email] = {
                            "name": entry.name,
                            "mobile_no": entry.mobile_no,
                            "suggestion":entry.suggestion,
                            "suggestion2":entry.suggestion2,
                            "questions": [],
                
                            "answers": []
                            }
                        grouped_data[entry.email]["questions"].append(entry.question)
       
                        grouped_data[entry.email]["answers"].append(entry.answer)

   
                    table_data = [["Email", "Name", "Mobile Number","Questions", "Answers","Suggestions1","Suggestions2"]]  # Header row
                    styles = getSampleStyleSheet()
    
                    for email, details in grouped_data.items():
                        questions = "<br/>".join([f"{i+1}. {q}" for i, q in enumerate(details["questions"])])
     
                        answers = "<br/>".join([f"{i+1}. {a}" for i, a in enumerate(details["answers"])])
        
                        table_data.append([
                        email,
                        details["name"],
                        details["mobile_no"],
            
            
                        Paragraph(questions, styles['Normal']),
 
                        Paragraph(answers, styles['Normal']),
                        details["suggestion"],
                        details["suggestion2"]
                        ])

   
                    table = Table(table_data, colWidths=[100, 100, 100,150,100,100,100])
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ]))


                    doc.build([table])
                    pdf_buffer.seek(0)
                    s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_S3_REGION_NAME)
                    folder_path = f"PostSurvey/"  # Define the folder path
                    file_key = f"{folder_path}PostSurveydata_{survey.id}.pdf" 
                    s3.upload_fileobj(pdf_buffer, settings.AWS_STORAGE_BUCKET_NAME,file_key, ExtraArgs={'ContentType': 'application/pdf'})

    # Construct the PDF URL
                    pdf_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_key}"

                  
                   
                    # s3 = boto3.client('s3',
                    #   aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    #   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    #   region_name=settings.AWS_S3_REGION_NAME)

                    # with open(pdf_filepath, 'rb') as pdf_file:
                    #     s3.upload_fileobj(pdf_file, settings.AWS_STORAGE_BUCKET_NAME, pdf_filename)
                        
                    # pdf_url = f"{settings.MEDIA_URL}{pdf_filename}"
                    survey.pdf_link = pdf_url
                    survey.submission_count=len(list(set(post.email for post in data)))
                    survey.save()
                    data.delete()
                    
                    
                    
#----------------------------------------------------------------------------------------------------MID--------------------------------------------           
                    
                    
                if survey.survey_type=="MID":
                    # pdf_filename = f"MidSurveydata_{survey.id}.pdf"
                    # pdf_filepath = os.path.join(settings.MEDIA_ROOT, pdf_filename)
                    pdf_buffer = io.BytesIO()

                    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)

    
                    data = QuestionAnswer.objects.all().order_by('email')

    
                    grouped_data = {}
                    for entry in data:
                        if entry.email not in grouped_data:
                            grouped_data[entry.email] = {
                            "name": entry.name,
                            "mobile_no": entry.mobile_no,
                            "questions": [],
                            "answers": []
                             }
                        grouped_data[entry.email]["questions"].append(entry.question)
       
                        grouped_data[entry.email]["answers"].append(entry.answer)

    
                    table_data = [["Email", "Name", "Mobile Number", "Questions", "Answers"]]  # Header row
                    styles = getSampleStyleSheet()
    
                    for email, details in grouped_data.items():
                        questions = "<br/>".join([f"{i+1}. {q}" for i, q in enumerate(details["questions"])])
        
                        answers = "<br/>".join([f"{i+1}. {a}" for i, a in enumerate(details["answers"])])
       
                        table_data.append([
                                    email,
                                    details["name"],
                                    details["mobile_no"],
                                    Paragraph(questions, styles['Normal']),

                                    Paragraph(answers, styles['Normal'])
                                  ])

                    table = Table(table_data, colWidths=[100, 100, 100, 200,100])
                    table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black),
                             ]))

  
                    doc.build([table])
                    pdf_buffer.seek(0)
                    s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_S3_REGION_NAME)
                    folder_path = f"MidSurvey/"  # Define the folder path
                    file_key = f"{folder_path}MidtSurveydata_{survey.id}.pdf" 
                    s3.upload_fileobj(pdf_buffer, settings.AWS_STORAGE_BUCKET_NAME,file_key, ExtraArgs={'ContentType': 'application/pdf'})

    # Construct the PDF URL
                    pdf_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_key}"

                  

    # Construct the PDF URL
                    
                    # s3 = boto3.client('s3',
                    #   aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    #   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    #   region_name=settings.AWS_S3_REGION_NAME)

                    # with open(pdf_filepath, 'rb') as pdf_file:
                    #     s3.upload_fileobj(pdf_file, settings.AWS_STORAGE_BUCKET_NAME, pdf_filename)
                        
                    # pdf_url = f"{settings.MEDIA_URL}{pdf_filename}"

    
                    survey.pdf_link = pdf_url
                    survey.submission_count=len(list(set(post.email for post in data)))
                    survey.save()
                    data.delete()

                    
    
 

 
                
                
                count=len(SurveyTable.objects.all())
                
                return Response({'message':'Survey created successfully','data':serializer.data,'lenght_of_survey_table':count,'status':status.HTTP_200_OK},status.HTTP_200_OK)
            
            else:
                return Response({'message':serializer.errors,'status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({'error':str(e),'status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
class getAllSurvey(APIView):
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
            tokens=AdminTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None and tokens is None:
                return Response({'error':"Token is required",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            
            if id is None:
                survey=SurveyTable.objects.all().order_by('-id')
                count=len(SurveyTable.objects.all())
                
                serializer=SurveySerializer(survey,many=True)
                
                if serializer:
                    return Response({'message':'All survey data retrieves successfully','data':serializer.data,'lenght_of_survey_table':count,'status':status.HTTP_200_OK},status.HTTP_200_OK)
                
                else:
                    return Response(serializer.errors,status=404)
                    
        except Exception as e:
            return Response({'data':str(e),'status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class getAllTypeSurvey(APIView):
    def get(self,request,Surv_type=None):
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
                return Response({'error':"Token is required",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            if Surv_type is None:
                return Response({'error':"Survey type required",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
         
            survey=SurveyTable.objects.filter(survey_type=Surv_type).all()
            count=len(SurveyTable.objects.filter(survey_type=Surv_type).all())
            if not survey:
                return Response({'error':"Survey type not found in survey table",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
                
            serializer=SurveySerializer(survey,many=True)
                
            if serializer:
                return Response({'message':'All survey type retrieves successfully','data':serializer.data,'submission_count':count,'status':status.HTTP_200_OK},status.HTTP_200_OK)
                
            else:
                return Response(serializer.errors,status=404)
                    
        except Exception as e:
            return Response({'data':str(e),'status':status.HTTP_500_INTERNAL_SERVER_ERROR},status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            
        
class updateSurvey(APIView):
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
            survey=SurveyTable.objects.filter(id=id).first()
            if not survey:
                return Response({'error':"Survey not found",'status':status.HTTP_400_BAD_REQUEST},status.HTTP_400_BAD_REQUEST)
            
            serializer=SurveySerializer(survey,data=request.data,partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Information updated successfully','data':serializer.data,'status':status.HTTP_200_OK},status.HTTP_200_OK)
            
            else:
                return Response({'error':serializer.errors},status=400)
            
            
        except Exception as e:
            return Response({'error':str(e)},status=500)
        
        
class deleteSurvey(APIView):
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
            token_instance = UserTokenTable.objects.filter(user_id=userId).all()
            tokens=AdminTokenTable.objects.filter(user_id=userId).all()
            if token_instance is None and tokens is None:
                return Response({'error':"Token not found",'status':status.HTTP_404_NOT_FOUND},status.HTTP_404_NOT_FOUND)
            if id is None:
                survey=SurveyTable.objects.all()
            
            elif id:
                survey=SurveyTable.objects.filter(id=id).first()
            if not survey:
                return Response({'message':"Survey table is empty",'status':status.HTTP_200_OK},status.HTTP_200_OK)
                

            
            serializer=SurveySerializer(survey,many=True)
            survey.delete()
          
            if serializer:
               
                return Response({'message':'Survey deleted successfully','status':status.HTTP_200_OK},status.HTTP_200_OK)
            
            else:
                return Response({'error':serializer.errors},status=400)
            
            
        except Exception as e:
            return Response({'error':str(e)},status=500)

            
        
        
        
    
    
