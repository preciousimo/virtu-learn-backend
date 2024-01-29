from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from .serializers import *
from .models import *

class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    # permission_classes = [permissions.IsAuthenticated]

class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    
class TeacherDashboard(generics.RetrieveAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherDashboardSerializer

@csrf_exempt
def teacher_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        teacherData = Teacher.objects.get(email=email, password=password)
        if teacherData:
            return JsonResponse({'bool': True, 'teacher_id': teacherData.id})
        else:
            return JsonResponse({'bool': False})
    except Teacher.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Invalid Input'})

    
class CategoryList(generics.ListCreateAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CategorySerializer
    
class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    def get_queryset(self):
        qs=super().get_queryset()
        if 'result' in self.request.GET:
            limit=int(self.request.GET['result'])
            qs=Course.objects.all().order_by('-id')[:limit]
            
        if 'category' in self.request.GET:
            category=self.request.GET['category']
            qs=Course.objects.filter(techs__icontains=category)
            
        if 'skill_name' in self.request.GET and 'teacher' in self.request.GET:
            skill_name=self.request.GET['skill_name']
            teacher=self.request.GET['teacher']
            teacher=Teacher.objects.filter(id=teacher).first()
            qs=Course.objects.filter(techs__icontains=skill_name, teacher=teacher)
            
        elif 'studentId' in self.kwargs:
            student_id = self.kwargs['studentId']
            student = Student.objects.get(pk=student_id)
            queries = [Q(techs__iendswith=value) for value in student.interested_categories]
            query = queries.pop()
            for item in queries:
                query |= item
            qs = Course.objects.filter(query)
            return qs
        return qs
    
class CourseDetailView(generics.RetrieveAPIView):
    queryset=Course.objects.all()
    serializer_class=CourseSerializer
    
class TeacherCourseList(generics.ListAPIView):
    serializer_class = CourseSerializer
    
    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = Teacher.objects.get(pk=teacher_id)
        return Course.objects.filter(teacher=teacher)
    
class TeacherCourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class ChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

class CourseChapterList(generics.ListCreateAPIView):
    serializer_class = ChapterSerializer
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = get_object_or_404(Course, pk=course_id)
        return Chapter.objects.filter(course=course)

class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # permission_classes = [permissions.IsAuthenticated]

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

@csrf_exempt
def student_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        studentData = Student.objects.get(email=email, password=password)
        if studentData:
            return JsonResponse({'bool': True, 'student_id': studentData.id})
        else:
            return JsonResponse({'bool': False})
    except Student.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Invalid Input'})
    
class StudentEnrollCourseList(generics.ListCreateAPIView):
    queryset = StudentCourseEnrollment.objects.all()
    serializer_class = StudentCourseEnrollSerializer

@csrf_exempt
def fetch_enroll_status(request, student_id, course_id):
    try:
        student=Student.objects.filter(id=student_id).first()
        course=Course.objects.filter(id=course_id).first()
        enrollStatus=StudentCourseEnrollment.objects.filter(course=course, student=student).count()
        if enrollStatus:
            return JsonResponse({'bool': True})
        else:
            return JsonResponse({'bool': False})
    except Student.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Invalid Input'})
    
class StudentFavouriteCourseList(generics.ListCreateAPIView):
    queryset = StudentFavouriteCourse.objects.all()
    serializer_class = StudentFavouriteCourseSerializer
    
    def get_queryset(self):
        if 'student_id' in self.kwargs:
            student_id = self.kwargs['student_id']
            student = get_object_or_404(Student, pk=student_id)
            return StudentFavouriteCourse.objects.filter(student=student).distinct()

@csrf_exempt  
def fetch_favourite_status(request, student_id, course_id):
    student=Student.objects.filter(id=student_id).first()
    course=Course.objects.filter(id=course_id).first()
    favouriteStatus=StudentFavouriteCourse.objects.filter(course=course, student=student).first()
    if favouriteStatus and favouriteStatus.status == True:
        return JsonResponse({'bool': True})
    else:
        return JsonResponse({'bool': False})

@csrf_exempt   
def remove_favourite_course(request, course_id, student_id):
    student=Student.objects.filter(id=student_id).first()
    course=Course.objects.filter(id=course_id).first()
    favouriteStatus=StudentFavouriteCourse.objects.filter(course=course, student=student).delete()
    if favouriteStatus:
        return JsonResponse({'bool': True})
    else:
        return JsonResponse({'bool': False})

class EnrolledStudentList(generics.ListAPIView):
    queryset = StudentCourseEnrollment.objects.all()
    serializer_class = StudentCourseEnrollSerializer
    
    def get_queryset(self):
        if 'course_id' in self.kwargs:
            course_id = self.kwargs['course_id']
            course = get_object_or_404(Course, pk=course_id)
            return StudentCourseEnrollment.objects.filter(course=course)
        elif 'teacher_id' in self.kwargs:
            teacher_id = self.kwargs['teacher_id']
            teacher = get_object_or_404(Teacher, pk=teacher_id)
            return StudentCourseEnrollment.objects.filter(course__teacher=teacher).distinct()
        elif 'student_id' in self.kwargs:
            student_id = self.kwargs['student_id']
            student = get_object_or_404(Student, pk=student_id)
            return StudentCourseEnrollment.objects.filter(student=student).distinct()
    
class CourseRatingList(generics.ListCreateAPIView):
    queryset = CourseRating.objects.all()
    serializer_class = CourseRatingSerializer

@csrf_exempt
def fetch_rating_status(request, student_id, course_id):
    try:
        student=Student.objects.filter(id=student_id).first()
        course=Course.objects.filter(id=course_id).first()
        ratingStatus=CourseRating.objects.filter(course=course, student=student).count()
        if ratingStatus:
            return JsonResponse({'bool': True})
        else:
            return JsonResponse({'bool': False})
    except Student.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Invalid Input'})

@csrf_exempt
def teacher_change_password(request, teacher_id):
    password = request.POST.get('password')
    try:
        teacherData = Teacher.objects.get(id=teacher_id)
        if teacherData:
            teacherData.password = password
            teacherData.save()
            return JsonResponse({'bool': True})
        else:
            return JsonResponse({'bool': False})
    except Teacher.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Invalid Input'})
    
@csrf_exempt
def student_change_password(request, student_id):
    password = request.POST.get('password')
    try:
        studentData = Student.objects.get(id=student_id)
        if studentData:
            studentData.password = password
            studentData.save()
            return JsonResponse({'bool': True})
        else:
            return JsonResponse({'bool': False})
    except Teacher.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Invalid Input'})
    
    
class AssignmentList(generics.ListCreateAPIView):
    queryset = StudentAssignment.objects.all()
    serializer_class = StudentAssignmentSerializer
    
    def get_queryset(self):
        student_id = self.kwargs['student_id']
        teacher_id = self.kwargs['teacher_id']
        student = get_object_or_404(Student, pk=student_id)
        teacher = get_object_or_404(Teacher, pk=teacher_id)
        return Chapter.objects.filter(student=student, teacher=teacher)

