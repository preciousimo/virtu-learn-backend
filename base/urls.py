from django.urls import path
from .views import*

urlpatterns = [
    path('teacher/', TeacherList.as_view(), name='teacher'),
    path('teacher/<int:pk>/', TeacherDetail.as_view(), name='teacher_detail'),
]
