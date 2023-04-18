from django.db import models

# Teacher model
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    image = models.ImageField(upload_to='teacher_image', blank=True)

    class Meta:
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return self.name
    
# Subject category model
class SubjectCategory(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Subject Categories'

    def __str__(self):
        return self.title
    
# Subject model
class Subject(models.Model):
    category = models.ForeignKey(SubjectCategory, on_delete=models.CASCADE)
    Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.title
    
# Class model
class Class(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    form_tutor = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Classes'

    def __str__(self):
        return self.name
    
# Student model
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    image = models.ImageField(upload_to='student_image', blank=True)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.name