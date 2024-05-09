from rest_framework import serializers
from .models import QuestionAnswer



class QuestionSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = QuestionAnswer
        fields =['id','question','hindi_question','answer']


