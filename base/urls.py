from django.urls import path
from .views import *

urlpatterns = [
    path('teacher/', TeacherList.as_view()),
    path('teacher/dashboard/<int:pk>/', TeacherDashboard.as_view()),
    path('teacher/<int:pk>/', TeacherDetail.as_view()),
    path('teacher/change-password/<int:teacher_id>/', teacher_change_password),
    path('teacher-login/', teacher_login),
    
    path('category/', CategoryList.as_view()),
    path('course/', CourseList.as_view()),
    path('search-courses/<str:searchstring>', CourseList.as_view()),
    path('course/<int:pk>', CourseDetailView.as_view()),
    path('chapter/<int:pk>', ChapterDetailView.as_view()),
    path('course-chapters/<int:course_id>', CourseChapterList.as_view()),
    
    path('teacher-courses/<int:teacher_id>', TeacherCourseList.as_view()),
    path('teacher-course-detail/<int:pk>', TeacherCourseDetail.as_view()),
    
    path('student/', StudentList.as_view()),
    path('student/dashboard/<int:pk>/', StudentDashboard.as_view()),
    path('student/<int:pk>/', StudentDetail.as_view()),
    path('student-login/', student_login),
    path('student/change-password/<int:student_id>/', student_change_password),
    
    path('student-enroll-course/', StudentEnrollCourseList.as_view()),
    path('fetch-enroll-status/<int:student_id>/<int:course_id>', fetch_enroll_status),
    path('fetch-all-enrolled-students/<int:teacher_id>', EnrolledStudentList.as_view()),
    path('fetch-enrolled-students/<int:course_id>', EnrolledStudentList.as_view()),
    path('fetch-enrolled-courses/<int:student_id>', EnrolledStudentList.as_view()),
    path('fetch-recommended-courses/<int:studentId>', CourseList.as_view()),
    path('course-rating/<int:course_id>', CourseRatingList.as_view()),
    path('fetch-rating-status/<int:student_id>/<int:course_id>', fetch_rating_status),
    path('student-add-favourite-course/', StudentFavouriteCourseList.as_view()),
    path('student-remove-favourite-course/<int:course_id>/<int:student_id>', remove_favourite_course),
    path('fetch-favourite-status/<int:student_id>/<int:course_id>', fetch_favourite_status),
    path('fetch-favourite-courses/<int:student_id>', StudentFavouriteCourseList.as_view()),
    path('student-assignment/<int:teacher_id>/<int:student_id>', AssignmentList.as_view()),
    path('my-assignments/<int:studentId>', MyAssignmentList.as_view()),
    path('update-assignment/<int:pk>', UpdateAssignment.as_view()),
    path('student/fetch-all-notifications/<int:studentId>', NotificationList.as_view()),
    path('save-notifications/', NotificationList.as_view()),
    
    path('quiz/', QuizList.as_view()),
    path('teacher-quiz/<int:teacher_id>', TeacherQuizList.as_view()),
    path('teacher-quiz-detail/<int:pk>', TeacherQuizDetail.as_view()),
    path('quiz/<int:pk>', QuizDetailView.as_view()),
    path('quiz-questions/<int:quiz_id>', QuizQuestionList.as_view()),
    path('quiz-questions/<int:quiz_id>/<int:limit>', QuizQuestionList.as_view()),
    path('fetch-quiz-assign-status/<int:quiz_id>/<int:course_id>', fetch_quiz_assign_status),
    path('quiz-assign-course/', CourseQuizList.as_view()),
    path('fetch-assigned-quiz/<int:course_id>', CourseQuizList.as_view()),
    path('attempt-quiz/', AttemptQuizList.as_view()),
    path('quiz-questions/<int:quiz_id>/next-question/<int:question_id>', QuizQuestionList.as_view()),
    path('fetch-quiz-attempt-status/<int:quiz_id>/<int:student_id>', fetch_quiz_attempt_status),
    
    path('study-materials/<int:course_id>', StudyMaterialsList.as_view()),
    path('study-material/<int:pk>', StudyMaterialDetailView.as_view()),
    path('student/study-materials/<int:course_id>', StudyMaterialsList.as_view()),
    
]
