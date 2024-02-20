from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.mail import send_mail, EmailMessage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from .models import *


# Pagination Class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 4


# Teacher related views
class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    
    def get_queryset(self):
        if 'popular' in self.request.GET:
            sql = "SELECT *, COUNT(c.id) as total_course FROM base_teacher as t INNER JOIN base_course as c ON c.teacher_id=t.id GROUP BY t.id ORDER BY total_course desc"
            return Teacher.objects.raw(sql)


class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherDashboard(generics.RetrieveAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherDashboardSerializer


@csrf_exempt
def teacher_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        teacherData = Teacher.objects.get(email=email, password=password)
        if teacherData:
            if not teacherData.verify_status:
                return JsonResponse({'bool': False, 'msg': 'Account is not verified!!'})
            else:
                return JsonResponse({'bool': True, 'teacher_id': teacherData.id})
        else:
            return JsonResponse({'bool': False, 'msg': 'Invalid Email or Password!'})
    except Teacher.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Invalid Input'})


@csrf_exempt
def verify_teacher_via_otp(request, teacher_id):
    otp_digit = request.POST.get('otp_digit')
    teacher = Teacher.objects.filter(id=teacher_id, otp_digit=otp_digit).first()
    if teacher:
        teacher.verify_status = True
        teacher.save()
        return JsonResponse({'bool': True, 'teacher_id': teacher.id})
    else:
        return JsonResponse({'bool': False})


# Category related views
class CategoryList(generics.ListCreateAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CategorySerializer


# Course related views
class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = super().get_queryset()

        if 'result' in self.request.GET:
            limit = int(self.request.GET['result'])
            qs = Course.objects.all().order_by('-id')[:limit]

        elif 'category' in self.request.GET:
            category_id = self.request.GET['category']
            category = CourseCategory.objects.filter(id=category_id).first()
            qs = Course.objects.filter(techs__icontains=category)

        elif 'skill_name' in self.request.GET and 'teacher' in self.request.GET:
            skill_name = self.request.GET['skill_name']
            teacher_id = self.request.GET['teacher']
            teacher = Teacher.objects.filter(id=teacher_id).first()
            qs = Course.objects.filter(techs__icontains=skill_name, teacher=teacher)

        elif 'searchstring' in self.request.GET:
            search = self.request.GET['searchstring']
            if search:
                qs = Course.objects.filter(
                    Q(title__icontains=search) |
                    Q(techs__icontains=search)
                )

        elif 'studentId' in self.kwargs:
            student_id = self.kwargs['studentId']
            student = Student.objects.get(pk=student_id)
            queries = [Q(techs__iendswith=value) for value in student.interested_categories]
            query = queries.pop()
            for item in queries:
                query |= item
            qs = Course.objects.filter(query)
            return qs

        return qs


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class TeacherCourseList(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = Teacher.objects.get(pk=teacher_id)
        return Course.objects.filter(teacher=teacher)


class TeacherCourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# Chapter related views
class ChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['chapter_duration'] = self.chapter_duration
        return context


class CourseChapterList(generics.ListCreateAPIView):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = get_object_or_404(Course, pk=course_id)
        return Chapter.objects.filter(course=course)


# Student related views
class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDashboard(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentDashboardSerializer


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


@csrf_exempt
def student_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        studentData = Student.objects.get(email=email, password=password)
        if studentData:
            return JsonResponse({'bool': True, 'student_id': studentData.id})
        else:
            return JsonResponse({'bool': False})
    except Student.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Invalid Input'})


class StudentEnrollCourseList(generics.ListCreateAPIView):
    queryset = StudentCourseEnrollment.objects.all()
    serializer_class = StudentCourseEnrollSerializer


def fetch_enroll_status(request, student_id, course_id):
    try:
        student = Student.objects.filter(id=student_id).first()
        course = Course.objects.filter(id=course_id).first()
        enrollStatus = StudentCourseEnrollment.objects.filter(course=course, student=student).count()
        if enrollStatus:
            return JsonResponse({'bool': True})
        else:
            return JsonResponse({'bool': False})
    except Student.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Invalid Input'})


class StudentFavouriteCourseList(generics.ListCreateAPIView):
    queryset = StudentFavouriteCourse.objects.all()
    serializer_class = StudentFavouriteCourseSerializer

    def get_queryset(self):
        if 'student_id' in self.kwargs:
            student_id = self.kwargs['student_id']
            student = get_object_or_404(Student, pk=student_id)
            return StudentFavouriteCourse.objects.filter(student=student).distinct()


def fetch_favourite_status(request, student_id, course_id):
    student = Student.objects.filter(id=student_id).first()
    course = Course.objects.filter(id=course_id).first()
    favouriteStatus = StudentFavouriteCourse.objects.filter(course=course, student=student).first()
    if favouriteStatus and favouriteStatus.status == True:
        return JsonResponse({'bool': True})
    else:
        return JsonResponse({'bool': False})


@csrf_exempt
def remove_favourite_course(request, course_id, student_id):
    student = Student.objects.filter(id=student_id).first()
    course = Course.objects.filter(id=course_id).first()
    favouriteStatus = StudentFavouriteCourse.objects.filter(course=course, student=student).delete()
    if favouriteStatus:
        return JsonResponse({'bool': True})
    else:
        return JsonResponse({'bool': False})


class EnrolledStudentList(generics.ListAPIView):
    queryset = StudentCourseEnrollment.objects.all()
    serializer_class = StudentCourseEnrollSerializer

    def get_queryset(self):
        if 'course_id' in self.kwargs:
            course_id = self.kwargs['course_id']
            course = get_object_or_404(Course, pk=course_id)
            return StudentCourseEnrollment.objects.filter(course=course)
        elif 'teacher_id' in self.kwargs:
            teacher_id = self.kwargs['teacher_id']
            teacher = get_object_or_404(Teacher, pk=teacher_id)
            return StudentCourseEnrollment.objects.filter(course__teacher=teacher).distinct()
        elif 'student_id' in self.kwargs:
            student_id = self.kwargs['student_id']
            student = get_object_or_404(Student, pk=student_id)
            return StudentCourseEnrollment.objects.filter(student=student).distinct()


class CourseRatingList(generics.ListCreateAPIView):
    queryset = CourseRating.objects.all()
    serializer_class = CourseRatingSerializer

    def get_queryset(self):
        if 'popular' in self.request.GET:
            sql = "SELECT *, AVG(cr.rating) as avg_rating FROM base_courserating as cr INNER JOIN base_course as c ON cr.course_id=c.id GROUP BY c.id ORDER BY avg_rating desc LIMIT 4"
            return CourseRating.objects.raw(sql)
        if 'all' in self.request.GET:
            sql = "SELECT *, AVG(cr.rating) as avg_rating FROM base_courserating as cr INNER JOIN base_course as c ON cr.course_id=c.id GROUP BY c.id ORDER BY avg_rating desc"
            return CourseRating.objects.raw(sql)
        return CourseRating.objects.filter(course__isnull=False).order_by('-rating')


def fetch_rating_status(request, student_id, course_id):
    try:
        student = Student.objects.filter(id=student_id).first()
        course = Course.objects.filter(id=course_id).first()
        ratingStatus = CourseRating.objects.filter(course=course, student=student).count()
        if ratingStatus:
            return JsonResponse({'bool': True})
        else:
            return JsonResponse({'bool': False})
    except Student.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Invalid Input'})


@csrf_exempt
def teacher_change_password(request, teacher_id):
    password = request.POST.get('password')
    try:
        teacherData = Teacher.objects.get(id=teacher_id)
        if teacherData:
            teacherData.password = password
            teacherData.save()
            return JsonResponse({'bool': True})
        else:
            return JsonResponse({'bool': False})
    except Teacher.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Invalid Input'})


@csrf_exempt
def student_change_password(request, student_id):
    password = request.POST.get('password')
    try:
        studentData = Student.objects.get(id=student_id)
        if studentData:
            studentData.password = password
            studentData.save()
            return JsonResponse({'bool': True})
        else:
            return JsonResponse({'bool': False})
    except Teacher.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Invalid Input'})


# Assignment related views
class AssignmentList(generics.ListCreateAPIView):
    queryset = StudentAssignment.objects.all()
    serializer_class = StudentAssignmentSerializer

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        teacher_id = self.kwargs['teacher_id']
        student = get_object_or_404(Student, pk=student_id)
        teacher = get_object_or_404(Teacher, pk=teacher_id)
        return StudentAssignment.objects.filter(student=student, teacher=teacher)


class MyAssignmentList(generics.ListCreateAPIView):
    queryset = StudentAssignment.objects.all()
    serializer_class = StudentAssignmentSerializer

    def get_queryset(self):
        student_id = self.kwargs['studentId']
        student = get_object_or_404(Student, pk=student_id)
        Notification.objects.filter(student=student, notif_for='student', notif_subject='assignment').update(
            notif_read_status=True)
        return StudentAssignment.objects.filter(student=student)


class UpdateAssignment(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentAssignment.objects.all()
    serializer_class = StudentAssignmentSerializer


class NotificationList(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        student_id = self.kwargs['studentId']
        student = get_object_or_404(Student, pk=student_id)
        Notification.objects.filter(student=student, notif_for='student', notif_subject='assignment').update(
            notif_read_status=True)
        return Notification.objects.filter(student=student, notif_for='student', notif_subject='assignment')


# Quiz related views
class QuizList(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class TeacherQuizList(generics.ListAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = Teacher.objects.get(pk=teacher_id)
        return Quiz.objects.filter(teacher=teacher)


class TeacherQuizDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizQuestionList(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        quiz_id = self.kwargs['quiz_id']
        quiz = Quiz.objects.get(pk=quiz_id)
        if 'limit' in self.kwargs:
            return QuizQuestions.objects.filter(quiz=quiz).order_by('id')[:1]
        elif 'question_id' in self.kwargs:
            current_question = self.kwargs['question_id']
            return QuizQuestions.objects.filter(quiz=quiz, id__gt=current_question).order_by('id')[:1]
        else:
            return QuizQuestions.objects.filter(quiz=quiz)


class CourseQuizList(generics.ListCreateAPIView):
    queryset = CourseQuiz.objects.all()
    serializer_class = CourseQuizSerializer

    def get_queryset(self):
        if 'course_id' in self.kwargs:
            course_id = self.kwargs['course_id']
            course = get_object_or_404(Course, pk=course_id)
            return CourseQuiz.objects.filter(course=course)


def fetch_quiz_assign_status(request, quiz_id, course_id):
    quiz = Quiz.objects.filter(id=quiz_id).first()
    course = Course.objects.filter(id=course_id).first()
    assigStatus = CourseQuiz.objects.filter(course=course, quiz=quiz).count()
    if assigStatus:
        return JsonResponse({'bool': True})
    else:
        return JsonResponse({'bool': False})


class AttemptQuizList(generics.ListCreateAPIView):
    queryset = AttemptQuiz.objects.all()
    serializer_class = AttemptQuizSerializer

    def get_queryset(self):
        if 'quiz_id' in self.kwargs:
            quiz_id = self.kwargs['quiz_id']
            quiz = Quiz.objects.get(pk=quiz_id)
            return AttemptQuiz.objects.raw(f'SELECT * FROM base_attemptquiz WHERE quiz_id={int(quiz_id)} GROUP by student_id')


def fetch_quiz_attempt_status(request, quiz_id, student_id):
    quiz = Quiz.objects.filter(id=quiz_id).first()
    student = Student.objects.filter(id=student_id).first()
    attemptStatus = AttemptQuiz.objects.filter(student=student, question__quiz=quiz).count()
    if attemptStatus > 0:
        return JsonResponse({'bool': True})
    else:
        return JsonResponse({'bool': False})


def fetch_quiz_result(request, quiz_id, student_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    student = get_object_or_404(Student, id=student_id)
    total_questions = QuizQuestions.objects.filter(quiz=quiz).count()
    total_attempted_questions = AttemptQuiz.objects.filter(quiz=quiz, student=student).count()
    attempted_questions = AttemptQuiz.objects.filter(quiz=quiz, student=student)

    total_correct_questions = 0
    for attempt in attempted_questions:
        if attempt.right_ans == attempt.question.right_ans:
            total_correct_questions += 1

    return JsonResponse({
        'total_questions': total_questions,
        'total_attempted_questions': total_attempted_questions,
        'total_correct_questions': total_correct_questions
    })


# Other views
class StudyMaterialsList(generics.ListCreateAPIView):
    serializer_class = StudyMaterialSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = get_object_or_404(Course, pk=course_id)
        return StudyMaterial.objects.filter(course=course)


class StudyMaterialDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudyMaterial.objects.all()
    serializer_class = StudyMaterialSerializer


@csrf_exempt
def update_view(request, course_id):
    queryset = Course.objects.filter(pk=course_id).first()
    queryset.course_views += 1
    queryset.save()
    return JsonResponse({'views': queryset.course_views})


class FaqList(generics.ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FaqSerializer


class ContactList(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


@csrf_exempt
def teacher_forgot_password(request):
    email = request.POST.get('email')
    verify = Teacher.objects.filter(email=email).first()
    if verify:
        link = f'http://localhost:3000/teacher-change-password/{verify.id}'
        subject = 'Forgot Password'
        message = f'Hello {verify.name},\n\nYour One Time Password (OTP) for verification is: {link}\n\nThank you,\nThe Team'
        from_email = settings.EMAIL_HOST_USER
        to_email = [verify.email]
        send_email = EmailMessage(subject, message, from_email, to_email)
        send_email.send(fail_silently=False)
        return JsonResponse({'bool': True, 'msg': 'Please check your email!'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Invalid Email!!'})


@csrf_exempt
def teacher_change_password(request, teacher_id):
    password = request.POST.get('password')
    verify = Teacher.objects.filter(id=teacher_id).first()
    if verify:
        verify.password = password
        verify.save()
        return JsonResponse({'bool': True, 'msg': 'Password has been changed'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Oops... Some Error Occured!!'})


@csrf_exempt
def save_teacher_student_msg(request, teacher_id, student_id):
    teacher = Teacher.objects.get(id=teacher_id)
    student = Student.objects.get(id=student_id)
    msg_text = request.POST.get('msg_text')
    msg_from = request.POST.get('msg_from')
    msgRes = TeacherStudentChat.objects.create(
        teacher=teacher,
        student=student,
        msg_text=msg_text,
        msg_from=msg_from,
    )
    if msgRes:
        return JsonResponse({'bool': True, 'msg': 'Message has been sent!'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Oops... Some Error Occured!!'})
    

class MessageList(generics.ListAPIView):
    queryset = TeacherStudentChat.objects.all()
    serializer_class = TeacherStudentChatSerializer
    
    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        student_id = self.kwargs['student_id']
        teacher = Teacher.objects.get(id=teacher_id)
        student = Student.objects.get(id=student_id)
        return TeacherStudentChat.objects.filter(teacher=teacher, student=student).exclude(msg_text='')