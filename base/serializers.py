from rest_framework import serializers
from .models import *

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [ 'id', 'name', 'email', 'password', 'qualification', 'mobile_no', 'skills']
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = [ 'id', 'title', 'description']
        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [ 'id', 'category', 'teacher', 'title', 'description', 'featured_img', 'techs']