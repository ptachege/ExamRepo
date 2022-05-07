from rest_framework import serializers
from .models import *

class AllExamsSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Exams
        fields = '__all__'