from django.db import models
from django.core.serializers import serialize

# Teacher model
class Teacher(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100) 
    password = models.CharField(max_length=100, blank=True, null=True)
    qualification = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=20)
    skills = models.TextField()
    profile_img = models.ImageField(upload_to='teacher_image', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Teachers'
        
    def skill_list(self):
        skill_list=self.skills.split(',')
        return skill_list
    
    def total_teacher_courses(self):
        total_courses=Course.objects.filter(teacher=self).count()
        return total_courses
    
    def total_teacher_chapters(self):
        total_chapters=Chapter.objects.filter(course__teacher=self).count()
        return total_chapters
    
    def total_teacher_students(self):
        total_students=StudentCourseEnrollment.objects.filter(course__teacher=self).count()
        return total_students

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
    
    def total_enrolled_students(self):
        total_enrolled_students=StudentCourseEnrollment.objects.filter(course=self).count()
        return total_enrolled_students
    
    def course_rating(self):
        course_rating=CourseRating.objects.filter(course=self).aggregate(avg_rating=models.Avg('rating'))
        return course_rating['avg_rating']

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
    password = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=20)
    interested_categories = models.TextField()
    profile_img = models.ImageField(upload_to='student_image', blank=True, null=True)
    
    def enrolled_courses(self):
        enrolled_courses=StudentCourseEnrollment.objects.filter(student=self).count()
        return enrolled_courses
    
    def favourite_courses(self):
        favourite_courses=StudentFavouriteCourse.objects.filter(student=self).count()
        return favourite_courses
    
    def complete_assignments(self):
        complete_assignments=StudentAssignment.objects.filter(student=self, student_status=True).count()
        return complete_assignments
    
    def pending_assignments(self):
        pending_assignments=StudentAssignment.objects.filter(student=self, student_status=False).count()
        return pending_assignments

    class Meta:
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.name
    
class StudentCourseEnrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_courses')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrolled_student')
    enrolled_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Enrolled Courses'

    def __str__(self):
        return f'{self.course}-{self.student}'
    
class StudentFavouriteCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Student Favourite Courses'

    def __str__(self):
        return f'{self.course}-{self.student}'
    
class CourseRating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rating = models.PositiveBigIntegerField(default=0)
    reviews = models.TextField(null=True)
    review_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.course}-{self.student}-{self.rating}'

class StudentAssignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    detail = models.TextField(null=True)
    student_status=models.BooleanField(default=False, null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Student Assignments'
    
    def __str__(self):
        return self.title
    
# Notification Model
class Notification(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    notif_subject=models.CharField(max_length=200, verbose_name='Notification Subject', null=True)
    notif_for=models.CharField(max_length=200, verbose_name='Notification For')
    notif_created_time=models.DateTimeField(auto_now_add=True)
    notif_read_status=models.BooleanField(default=False, verbose_name='Notification Status')
    
    
    class Meta:
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return self.notif_for
    