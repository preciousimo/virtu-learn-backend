from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
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

class ChapterList(generics.ListCreateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

class ChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

class CourseChapterList(generics.ListAPIView):
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