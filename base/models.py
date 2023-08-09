from django.db import models

# Teacher model
class Teacher(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=20)
    skills = models.CharField(max_length=200)
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
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.title
    
# Student model
class Student(models.Model):
    full_name = models.CharField(max_length=100)
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