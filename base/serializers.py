from rest_framework import serializers
from .models import *
        
from django.contrib.auth.hashers import make_password, check_password

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'detail', 'email', 'qualification', 'mobile_no', 'skills', 'password', 'teacher_courses', 'skill_list']
        depth=1
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(TeacherSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super(TeacherSerializer, self).update(instance, validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = [ 'id', 'title', 'description']
        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [ 'id', 'category', 'teacher', 'title', 'description', 'featured_img', 'techs', 'course_chapters', 'related_videos', 'tech_list']
        depth=1
        

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = [ 'id', 'course', 'title', 'description', 'video', 'remarks']
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'username', 'password', 'interested_categories']
        extra_kwargs = {'password': {'write_only': True}}
        
class StudentCourseEnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourseEnrollment
        fields = [ 'id', 'course', 'student', 'enrolled_time']
