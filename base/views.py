from django.shortcuts import render 
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
    # permission_classes = [permissions.IsAuthenticated]

@csrf_exempt
def teacher_login(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    try:
        teacherData=Teacher.objects.get(email=email,password=password)
        if teacherData:
            return JsonResponse({'bool':True})
        else:
            return JsonResponse({'bool':False})
    except:
        return JsonResponse({'status':'failed','message':'Invalid Input'})