

from .models import QuestionAnswer

import json
import logging
from django.http import JsonResponse
from .models import QuestionAnswer,PreQuestionAnswer,PostQuestionAnswer

logger = logging.getLogger(__name__)



#---------------------Mid Survey-------------------------------------------------------------------

def SubmitQuestions(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body

            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            mobile_no = data.get('mobile_no')
            # suggestion = data.get('suggestion')

            # Check if required fields are provided
            if not (name and email and mobile_no):
                return JsonResponse({'error': 'Please provide all required fields'}, status=400)
            

           
            questions_list = data.get('questions', [])
            
            for item in questions_list:
                question_text = item.get('question', '')
                # print('text',question_text)
                hindi_question_text = item.get('questionhindi', '')  # Assuming you want to save Hindi questions too
                correct_answer = item.get('answer', '')

                # Save question and answer
                qa = QuestionAnswer(question=question_text, hindi_question=hindi_question_text, answer=correct_answer,
                    name=name,
                    email=email,
                    mobile_no=mobile_no)
                    
            
                qa.save()

            return JsonResponse({'message': 'Questions submitted successfully'})
        except Exception as e:
            logger.error(f"Error occurred while saving question-answer pairs: {e}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import QuestionSerializer
class GetAllQuestion(APIView):
    def get(self,request,email=None):
        if email is None:
            return Response("please enter email")
        questions = QuestionAnswer.objects.filter(email=email).all()
        if not questions:
            return Response({'error':'Mid survey details not founds'},status=404)
        name=list(set(ques.name for ques in questions))
        email=list(set(ques.email for ques in questions))
        mobile_no=list(set(ques.mobile_no for ques in questions))
        # suggestion=list(set(ques.suggestion for ques in questions))

        
            
        questions_data = []
        for index, question in enumerate(questions, start=1):
            data = {
                'question_number': f'q{index}',
                'question': question.question,
                'hindi_question': question.hindi_question,
                'answer': question.answer,
                # Add more fields as needed
                 }
            questions_data.append(data)
            # for question in questions:
            #     data = {
            #         'question': question.question,
            #         'hindi_question': question.hindi_question,
            #         'answer': question.answer,
            #         # Add more fields as needed
            #     }
            #     questions_data.append(data)
          
        return JsonResponse({'data':questions_data,'name':name,'email':email,'mobileNo':mobile_no})
    
        
        

            
            
class deleteQuestions(APIView):
    def delete(self,request):
        questions=QuestionAnswer.objects.all()
        if not questions:
            return Response({'message':'Mid survey table already empty'},status=400)
        questions.delete()
        return Response("Successfull")
    
    
#-------------------------------------PRE  SURVEY---------------------------------------------------------------
    
def PreSubmitQuestions(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body

            data = json.loads(request.body)
           
            suggestion = data.get('suggestion')


            questions_list = data.get('questions', [])
            
            for item in questions_list:
                question_text = item.get('question', '')
                # print('text',question_text)
                hindi_question_text = item.get('questionhindi', '')  # Assuming you want to save Hindi questions too
                correct_answer = item.get('answer', '')

                # Save question and answer
                qa = PreQuestionAnswer(question=question_text, hindi_question=hindi_question_text, answer=correct_answer,
                    # name=name,
                    # email=email,
                    # mobile_no=mobile_no,
                    suggestion=suggestion)
                    
            
                qa.save()

            return JsonResponse({'message': 'Questions submitted successfully'})
        except Exception as e:
            logger.error(f"Error occurred while saving question-answer pairs: {e}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import QuestionSerializer
class GetAllPreQuestion(APIView):
    def get(self,request):

        questions = PreQuestionAnswer.objects.all()
        if not questions:
            return Response({'error':'Pre survey details not founds'},status=404)
            
        suggestion=list(set(q.suggestion for q in questions))
            
        questions_data = []
        for index, question in enumerate(questions, start=1):
            data = {
                'question_number': f'q{index}',
                'question': question.question,
                'hindi_question': question.hindi_question,
                'answer': question.answer,
                # Add more fields as needed
                 }
            questions_data.append(data)

          
        return JsonResponse({'data':questions_data,'suggestion':suggestion})
    
        
        

            
            
class deletePreQuestions(APIView):
    def delete(self,request):
        questions=PreQuestionAnswer.objects.all()
        if not questions:
            return Response({'message':'Pre survey table already empty'},status=400)
        questions.delete()
        return Response("Successfull")
    
    
    
#-------------------------------------------------POST SURVEY-----------------------------------------------------------------
def PostSubmitQuestions(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body

            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            mobile_no = data.get('mobile_no')
            suggestion = data.get('suggestion')
            suggestion2= data.get('suggestion2')

            # Check if required fields are provided
            if not (name and email and mobile_no):
                return JsonResponse({'error': 'Please provide all required fields'}, status=400)
            

           
            questions_list = data.get('questions', [])
            
            for item in questions_list:
                question_text = item.get('question', '')
                # print('text',question_text)
                hindi_question_text = item.get('questionhindi', '')  # Assuming you want to save Hindi questions too
                correct_answer = item.get('answer', '')

                # Save question and answer
                qa = PostQuestionAnswer(question=question_text, hindi_question=hindi_question_text, answer=correct_answer,
                    name=name,
                    email=email,
                    mobile_no=mobile_no,suggestion=suggestion,suggestion2=suggestion2)
                    
            
                qa.save()

            return JsonResponse({'message': 'Questions submitted successfully'})
        except Exception as e:
            logger.error(f"Error occurred while saving question-answer pairs: {e}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import QuestionSerializer
class GetAllPostQuestion(APIView):
    def get(self,request,email=None):
        if email is None:
            return Response("please enter email")
        questions = PostQuestionAnswer.objects.filter(email=email).all()
        if not questions:
            return Response({'error':'Post survey details not founds'},status=404)
        name=list(set(ques.name for ques in questions))
        email=list(set(ques.email for ques in questions))
        mobile_no=list(set(ques.mobile_no for ques in questions))
        suggestion=list(set(ques.suggestion for ques in questions))
        suggestion2=list(set(ques.suggestion2 for ques in questions))
            
        questions_data = []
        for index, question in enumerate(questions, start=1):
            data = {
                'question_number': f'q{index}',
                'question': question.question,
                'hindi_question': question.hindi_question,
                'answer': question.answer,
                # Add more fields as needed
                 }
            questions_data.append(data)
            # for question in questions:
            #     data = {
            #         'question': question.question,
            #         'hindi_question': question.hindi_question,
            #         'answer': question.answer,
            #         # Add more fields as needed
            #     }
            #     questions_data.append(data)
          
        return JsonResponse({'data':questions_data,'name':name,'email':email,'mobileNo':mobile_no,'suggestion':suggestion,'suggestion2':suggestion2})
    
        
        

            
            
class deletePostQuestions(APIView):
    def delete(self,request):
        questions=PostQuestionAnswer.objects.all()
        if not questions:
            return Response({'message':'Post survey table already empty'},status=400)
        questions.delete()
        return Response("Successfull")
