from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from .forms import *
from .models import *
# from .utils import *

from django.db.models import Q


from django.http import FileResponse

import time
from random import sample


def Login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Username or Password is incorrect')
    return render(request, 'lms/login.html')

def Register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_student = True
            user.save()
            return redirect('login')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'lms/register.html')

def Logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def Dashboard(request):
    available_courses = []

    StudentCourse = CourseToStudent.objects.filter(student_id=request.user.student_id, is_approved=True)

    for i in StudentCourse:
        get_course = Course.objects.get(course_code=i.course_code)
        available_courses.append(get_course)

    global_announcement = GlobalAnnouncement.objects.all()

    if request.method == 'POST':
        course_code = request.POST.get('course_code')
        student_id = request.user.student_id

        is_exist = CourseToStudent.objects.get(course_code=course_code, student_id=student_id)

        if is_exist:
            return redirect('dashboard')
        else:
            CourseToStudent.objects.create(
                ciurse_code=course_code,
                student_id=student_id
            )
        return redirect('dashboard')

    context = {
        'courses': available_courses,
        'global_announcement': global_announcement
    }
    return render(request, 'lms/dashboard.html', context)

def Courses(request):
    return render(request, 'lms/courses.html')

def ApplyCourse(request, course_code):
    if request.user.is_student:
        if request.student_id == None:
            return redirect('profile')
        else:
            CourseToStudent.objects.create(
                course_code=course_code, 
                student_id=request.user.student_id
            )
    return redirect('dashboard')

def Modules(request, course_code):
    course = Course.objects.get(course_code=course_code)
    modules = CourseModule.objects.filter(course=course)

    context = {
        'modules': modules
    }

    return render(request, 'lms/student/modules.html', context)

def Profile(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CustomUserForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'lms/profile.html', context)

def CourseDetail(request, course_code):
    course = Course.objects.get(course_code=course_code)
    Announcement = CourseAnnouncement.objects.filter(course=course)

    context = {
        'announcements': Announcement,
        'course': course
    }
    return render(request, 'lms/student/course_detail.html', context)

def ModuleDetail(request):
    return render(request, 'lms/module_detail.html')

def Quizes(request, course_code):
    course = Course.objects.get(course_code=course_code)
    modules = Quiz.objects.filter(course=course).exclude(resultsquiz__student_id=request.user.student_id)

    context = {
        'quiz': modules
    }
    return render(request, 'lms/student/quizes.html', context)

def MultiChoice(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    all_questions = list(MultipleChoice.objects.all())
    selected_questions = sample(all_questions, int(quiz.multiple_choice))
    
    request.session['multiplequestions_ids'] = [question.id for question in selected_questions]

    print(selected_questions)
    print(quiz.course.course_code)

    context = {
        'quiz': quiz,
        'multiple_choices': selected_questions
    }

    return render(request, 'lms/student/multiple_choice_quiz.html', context)


def SubmitQuiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        correct_answers = 0
        total_questions = quiz.multiple_choice

        # Retrieve question IDs from session
        question_ids = request.session.get('multiplequestions_ids', [])
        questions = MultipleChoice.objects.filter(id__in=question_ids)

        # Check each submitted answer
        for idx, question in enumerate(questions, start=1):
            user_answer = request.POST.get(f'answer_{question.id}')
            if user_answer == question.answer:
                correct_answers += 1

        # Calculate score as a percentage
        score = (correct_answers / total_questions) * 100
        user = request.user
        user.total_points += correct_answers
        user.save()
        
        # Save the result
        ResultsQuiz.objects.create(
            student_id=request.user.student_id,
            quiz=quiz,
            score=score
        )
        
        return render(request, 'lms/student/quiz_results.html', {'quiz': quiz, 'score': score})

    return redirect('quiz_detail', quiz_id=quiz_id)

def PastQuizzes(request):
    modules = ResultsQuiz.objects.filter(student_id=request.user.student_id)

    context = {
        'quiz': modules
    }
    return render(request, 'lms/student/past_quiz.html', context)


def TrueFalse(request):
    return render(request, 'lms/true_false.html')

def FillBlank(request):
    return render(request, 'lms/fill_blank.html')

def QuizResult(request):
    return render(request, 'lms/quiz_result.html')




ROOMS = [
    (0, 'https://prod.spline.design/KSbWsM0OwrLYXyOO/scene.splinecode'),  # Basic Room
    (10, 'https://prod.spline.design/jL-hTvDQzuYPLpMf/scene.splinecode'),  # Only the PC
    (20, 'https://prod.spline.design/TJuTzrNT-TH0Z0sA/scene.splinecode'),  # No Music Box
    (30, 'https://prod.spline.design/BqtzOQtZajRZxXRV/scene.splinecode'),  # No Wall Deco
    (40, 'https://prod.spline.design/vHHH2LASfpWCrHXR/scene.splinecode'),  # No Trash and Speaker
    (50, 'https://prod.spline.design/a6qDWrFOtZ2DfsQh/scene.splinecode'),  # No Floor Deco
    (60, 'https://prod.spline.design/YpN1FUAW-5cAoYnP/scene.splinecode'),  # No Guitar
    (70, 'https://prod.spline.design/x-tRQs8TXauYtNgB/scene.splinecode'),  # No Chair Room
    (80, 'https://prod.spline.design/WC-O8efiVZxocK7P/scene.splinecode'),  # No Lamp Room
    (90, 'https://prod.spline.design/a7GTFzRLRz6DkNfd/scene.splinecode')   # Finish Room
]



# 3D Game
def Game3D(request):
    total_points = request.user.total_points

    # Determine the room to display based on total points
    room_url = ROOMS[0][1]  # Default to Basic Room
    for points, url in ROOMS:
        if total_points >= points:
            room_url = url

    context = {
        'room_url': room_url,
        'total_points': total_points
    }
    return render(request, 'lms/3d/game.html', context)


def AssetLink(request):
    assetlink = [
        {
            "relation": ["delegate_permission/common.handle_all_urls"],
            "target": {
            "namespace": "android_app",
            "package_name": "xyz.appmaker.zacrfh",
            "sha256_cert_fingerprints": ["0F:A1:A9:0E:25:08:3D:BD:60:BB:FC:5C:E4:76:BB:85:08:E6:C1:71:DF:21:C6:90:61:1D:28:A2:5D:88:C2:07"]
            }
        }
    ]

    return JsonResponse(assetlink, safe=False)