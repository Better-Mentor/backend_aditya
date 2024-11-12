
from rest_framework import serializers
from .models import Student, MCQ, Teacher, Class

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'grade_history_chart', 'reg_no']

class MCQSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQ
        fields = ['mcq_id', 'question', 'options', 'correct_option']

class TeacherClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['class_id', 'name']

class StudentInClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'reg_no']
