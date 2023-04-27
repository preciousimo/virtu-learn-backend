from rest_framework import serializers
from .models import *

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [ 'name', 'email', 'password', 'qualification', 'mobile_no', 'skills', 'image']