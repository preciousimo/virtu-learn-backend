from django.urls import path
from .views import TeacherList, TeacherDetail, teacher_login, CategoryList, CourseList

urlpatterns = [
    # Teacher
    path('teacher/', TeacherList.as_view()),
    path('teacher/<int:pk>/', TeacherDetail.as_view()),
    path('teacher-login/', teacher_login),
    # Category
    path('category/', CategoryList.as_view()),
    # Course
    path('course/', CourseList.as_view()),
]
