from django.db import models

class PreQuestion(models.Model):
    question_text = models.CharField(max_length=200)

class Option(models.Model):
    question = models.ForeignKey(PreQuestion, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=100)
    
class QuestionAnswer(models.Model):
    name = models.CharField(max_length=255,default='')
  
   
    mobile_no = models.CharField(max_length=15,default='')
   
    email = models.EmailField(default='')
    question = models.CharField(max_length=200)
    hindi_question = models.CharField(max_length=200,default='')
    answer = models.CharField(max_length=200) 