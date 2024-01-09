from django.urls import path
from .views import TeacherList, TeacherDetail, teacher_login, CategoryList, CourseList, TeacherCourseList, ChapterList, CourseChapterList

urlpatterns = [
    # Teacher
    path('teacher/', TeacherList.as_view()),
    path('teacher/<int:pk>/', TeacherDetail.as_view()),
    path('teacher-login/', teacher_login),
    # Category
    path('category/', CategoryList.as_view()),
    # Course
    path('course/', CourseList.as_view()),
    # Chapter
    path('chapter/', ChapterList.as_view()),
    # Specific Course Chapter
    path('course-chapters/<int:course_id>', CourseChapterList.as_view()),
    # Teacher Courses
    path('teacher-courses/<int:teacher_id>', TeacherCourseList.as_view()),
]
