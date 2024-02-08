from django.contrib import admin
from base.models import *

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile_no', 'profile_img']

class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['category', 'teacher', 'title']
    
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'video']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'username']
    
class StudentCourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['course', 'student']
    
class StudentFavouriteCourseAdmin(admin.ModelAdmin):
    list_display = ['course', 'student', 'status']
    
class CourseRatingtAdmin(admin.ModelAdmin):
    list_display = ['course', 'student', 'rating']
    
class StudentAssignmentAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'student', 'title']
    
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['notif_for', 'notif_read_status']


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentCourseEnrollment, StudentCourseEnrollmentAdmin)
admin.site.register(StudentFavouriteCourse, StudentFavouriteCourseAdmin)
admin.site.register(CourseRating, CourseRatingtAdmin)
admin.site.register(StudentAssignment, StudentAssignmentAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Quiz)
admin.site.register(QuizQuestions)
admin.site.register(CourseQuiz)
admin.site.register(AttemptQuiz)
admin.site.register(StudyMaterial)
admin.site.register(FAQ)
