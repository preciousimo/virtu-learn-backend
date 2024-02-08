from rest_framework import serializers
from .models import *
        
from django.contrib.auth.hashers import make_password, check_password

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'email', 'qualification', 'mobile_no', 'skills', 'profile_img',  'password', 'teacher_courses', 'skill_list', 'total_teacher_courses']
        extra_kwargs = {'password': {'write_only': True}}
    
    def __init__(self, *args, **kwargs):
        super(TeacherSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth=2


class TeacherDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [ 'total_teacher_courses', 'total_teacher_students', 'total_teacher_chapters']
        
    def __init__(self, *args, **kwargs):
        super(TeacherDashboardSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth=2
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = [ 'id', 'title', 'description']
        
    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth=2
        
        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [ 'id', 'category', 'teacher', 'title', 'description', 'featured_img', 'techs', 'course_chapters', 'related_videos', 'tech_list', 'total_enrolled_students', 'course_rating']
        
    def __init__(self, *args, **kwargs):
        super(CourseSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth=2
        

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = [ 'id', 'course', 'title', 'description', 'video', 'chapter_duration', 'remarks']
        
    def __init__(self, *args, **kwargs):
        super(ChapterSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth=2
        
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'username', 'password', 'profile_img', 'interested_categories']
        extra_kwargs = {'password': {'write_only': True}}
        
    def __init__(self, *args, **kwargs):
        super(StudentSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth=2
        
        
class StudentDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [ 'enrolled_courses', 'favourite_courses', 'complete_assignments', 'pending_assignments']
        
    def __init__(self, *args, **kwargs):
        super(StudentDashboardSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth=2
        
        
class StudentCourseEnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourseEnrollment
        fields = [ 'id', 'course', 'student', 'enrolled_time']
        
    def __init__(self, *args, **kwargs):
        super(StudentCourseEnrollSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth=2
            
            
class StudentFavouriteCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFavouriteCourse
        fields = [ 'id', 'course', 'student', 'status']
        
    def __init__(self, *args, **kwargs):
        super(StudentFavouriteCourseSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth=2
        
        
class CourseRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRating
        fields = [ 'id', 'course', 'student', 'rating', 'reviews', 'review_time']
        
    def __init__(self, *args, **kwargs):
        super(CourseRatingSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth=2
            

class StudentAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAssignment
        fields = [ 'id', 'teacher', 'student', 'title', 'detail', 'student_status', 'add_time']
        
    def __init__(self, *args, **kwargs):
        super(StudentAssignmentSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth=2
            

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['teacher', 'student', 'notif_subject', 'notif_for']
        
    def __init__(self, *args, **kwargs):
        super(NotificationSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth=2

         
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'teacher', 'title', 'detail', 'assign_status', 'add_time']
        
    def __init__(self, *args, **kwargs):
        super(QuizSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth=2


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestions
        fields = [ 'id', 'quiz', 'question', 'ans1', 'ans2', 'ans3', 'ans4', 'right_ans']
        
    def __init__(self, *args, **kwargs):
        super(QuestionSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth=2
  
            
class CourseQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseQuiz
        fields = [ 'id', 'course', 'quiz', 'add_time']
        
    def __init__(self, *args, **kwargs):
        super(CourseQuizSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth=2


class AttemptQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttemptQuiz
        fields = [ 'id', 'student', 'quiz', 'question', 'right_ans', 'add_time']
        
    def __init__(self, *args, **kwargs):
        super(AttemptQuizSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth=2


class StudyMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterial
        fields = [ 'id', 'course', 'title', 'description', 'upload', 'remarks']
        
    def __init__(self, *args, **kwargs):
        super(StudyMaterialSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth=2
            