from django.db import models
from django.core.serializers import serialize

# Teacher model
class Teacher(models.Model):
    name = models.CharField(max_length=100, null=True)
    detail = models.TextField(null=True)
    email = models.EmailField(max_length=100) 
    password = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=20)
    skills = models.TextField()
    image = models.ImageField(upload_to='teacher_image', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return self.name
    
# Course category model
class CourseCategory(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Course Categories'

    def __str__(self):
        return self.title
    
# Course model
class Course(models.Model):
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_courses')
    title = models.CharField(max_length=100)
    description = models.TextField()
    featured_img = models.ImageField(upload_to='course_imgs/', null=True)
    techs = models.TextField(null=True)

    class Meta:
        verbose_name_plural = 'Courses'
        
    def related_videos(self):
        related_videos=Course.objects.filter(techs__icontains=self.techs)
        return serialize('json', related_videos)
    
    def tech_list(self):
        tech_list=self.techs.split(',')
        return tech_list

    def __str__(self):
        return self.title
    
class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_chapters')
    title = models.CharField(max_length=100)
    description = models.TextField()
    video = models.FileField(upload_to='chapter_videos/', null=True)
    remarks = models.TextField(null=True)

    class Meta:
        verbose_name_plural = 'Chapters'

    def __str__(self):
        return self.title
    
# Student model
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    image = models.ImageField(upload_to='student_image', blank=True, null=True)
    interested_categories = models.TextField()

    class Meta:
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.name