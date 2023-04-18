from django.urls import path
from .views import*

urlpatterns = [
    path('teacher/', TeacherList.as_view(), name='teacher'),
]
