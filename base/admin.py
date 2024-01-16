from django.contrib import admin
from base.models import *

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile_no', 'image']

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
    
class CourseRatingtAdmin(admin.ModelAdmin):
    list_display = ['course', 'student', 'rating']




admin.site.register(Teacher, TeacherAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentCourseEnrollment, StudentCourseEnrollmentAdmin)
admin.site.register(CourseRating, CourseRatingtAdmin)
