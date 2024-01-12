from django.urls import path
from .views import TeacherList, TeacherDetail, teacher_login, CategoryList, CourseList, TeacherCourseList, ChapterDetailView, ChapterList, CourseChapterList, TeacherCourseDetail

urlpatterns = [
    path('teacher/', TeacherList.as_view()),
    path('teacher/<int:pk>/', TeacherDetail.as_view()),
    path('teacher-login/', teacher_login),
    
    path('category/', CategoryList.as_view()),
    path('course/', CourseList.as_view()),
    path('chapter/', ChapterList.as_view()),
    path('chapter/<int:pk>', ChapterDetailView.as_view()),
    path('course-chapters/<int:course_id>', CourseChapterList.as_view()),
    
    path('teacher-courses/<int:teacher_id>', TeacherCourseList.as_view()),
    path('teacher-course-detail/<int:pk>', TeacherCourseDetail.as_view()),
]
