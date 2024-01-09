from django.contrib import admin
from base.models import Teacher, CourseCategory, Course, Chapter, Student

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile_no', 'image']

class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['category', 'teacher', 'title']
    
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'videos']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile_no']




admin.site.register(Teacher, TeacherAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Student, StudentAdmin)
