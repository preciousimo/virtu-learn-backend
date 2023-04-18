from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import*
from .models import *

# Create your views here.
class TeacherList(APIView):
    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)
