from rest_framework import serializers
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from .models import *
import random


# Base Serializer
class BaseSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(BaseSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2


# Teacher Serializers
class TeacherSerializer(BaseSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'email', 'qualification', 'mobile_no', 'skills', 'profile_img', 'otp_digit', 'password', 'teacher_courses', 'skill_list', 'total_teacher_courses', 'linkedin_url', 'twitter_url', 'facebook_url', 'instagram_url', 'website_url']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        validated_data['otp_digit'] = otp
        
        instance = super(TeacherSerializer, self).create(validated_data)
        
        # Send email with OTP
        subject = 'OTP for Verification'
        message = f'Hello {instance.name},\n\nYour One Time Password (OTP) for verification is: {otp}\n\nThank you,\nThe Team'
        from_email = 'noreply@sonipstechmart.com'
        to_email = [instance.email]
        
        try:
            send_email = EmailMessage(subject, message, from_email, to_email)    
            send_email.send(fail_silently=False)
            # send_mail(subject, message, from_email, to_email)
        except Exception as e:
            instance.email_sent = False
            instance.save()
            print(f"Failed to send email to {instance.email}: {e}")
            raise serializers.ValidationError("Failed to send email. Please try again later.")
        
        return instance


class TeacherDashboardSerializer(BaseSerializer):
    class Meta:
        model = Teacher
        fields = ['total_teacher_courses', 'total_teacher_students', 'total_teacher_chapters']


# Course Serializers
class CategorySerializer(BaseSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'title', 'description', 'total_courses']
        
        
class CourseSerializer(BaseSerializer):
    class Meta:
        model = Course
        fields = ['id', 'category', 'teacher', 'title', 'description', 'featured_img', 'techs', 'course_chapters', 'related_videos', 'tech_list', 'total_enrolled_students', 'course_rating']


class ChapterSerializer(BaseSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'course', 'title', 'description', 'video', 'chapter_duration', 'remarks']


# Student Serializers
class StudentSerializer(BaseSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'username', 'password', 'profile_img', 'interested_categories']
        extra_kwargs = {'password': {'write_only': True}}


class StudentDashboardSerializer(BaseSerializer):
    class Meta:
        model = Student
        fields = ['enrolled_courses', 'favourite_courses', 'complete_assignments', 'pending_assignments']


class StudentCourseEnrollSerializer(BaseSerializer):
    class Meta:
        model = StudentCourseEnrollment
        fields = ['id', 'course', 'student', 'enrolled_time']


class StudentFavouriteCourseSerializer(BaseSerializer):
    class Meta:
        model = StudentFavouriteCourse
        fields = ['id', 'course', 'student', 'status']


# Rating and Review Serializers
class CourseRatingSerializer(BaseSerializer):
    class Meta:
        model = CourseRating
        fields = ['id', 'course', 'student', 'rating', 'reviews', 'review_time']


# Assignment Serializers
class StudentAssignmentSerializer(BaseSerializer):
    class Meta:
        model = StudentAssignment
        fields = ['id', 'teacher', 'student', 'title', 'detail', 'student_status', 'add_time']


class NotificationSerializer(BaseSerializer):
    class Meta:
        model = Notification
        fields = ['teacher', 'student', 'notif_subject', 'notif_for']


# Quiz Serializers
class QuizSerializer(BaseSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'teacher', 'title', 'detail', 'assign_status', 'add_time']


class QuestionSerializer(BaseSerializer):
    class Meta:
        model = QuizQuestions
        fields = ['id', 'quiz', 'question', 'ans1', 'ans2', 'ans3', 'ans4', 'right_ans']


class CourseQuizSerializer(BaseSerializer):
    class Meta:
        model = CourseQuiz
        fields = ['id', 'course', 'quiz', 'add_time']


# Attempt Quiz Serializer
class AttemptQuizSerializer(BaseSerializer):
    class Meta:
        model = AttemptQuiz
        fields = ['id', 'student', 'quiz', 'question', 'right_ans', 'add_time']


# Study Material Serializer
class StudyMaterialSerializer(BaseSerializer):
    class Meta:
        model = StudyMaterial
        fields = ['id', 'course', 'title', 'description', 'upload', 'remarks']


# FAQ Serializer
class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']


# Contact Serializer
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'message']


class TeacherStudentChatSerializer(BaseSerializer):
    class Meta:
        model = TeacherStudentChat
        fields = ['id', 'teacher', 'student', 'msg_from', 'msg_text', 'msg_time']
        
    def to_representation(self, instance):
        representation = super(TeacherStudentChatSerializer, self).to_representation(instance)
        representation['msg_time'] = instance.msg_time.strftime("%Y-%m-%d %H:%M")
        return representation