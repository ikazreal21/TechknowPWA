from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import *
from .models import *
# from .utils import *

from django.db.models import Q


from django.http import FileResponse

import time



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
    Courses = Course.objects.all()
    global_announcement = GlobalAnnouncement.objects.all()
    context = {
        'Courses': Courses,
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

def Modules(request):
    return render(request, 'lms/modules.html')

def Profile(request):
    return render(request, 'lms/profile.html')

def CourseDetail(request): 
    return render(request, 'lms/course_detail.html')

def ModuleDetail(request):
    return render(request, 'lms/module_detail.html')

def Quiz(request):
    return render(request, 'lms/quiz.html')

def QuizResult(request):
    return render(request, 'lms/quiz_result.html')

def MultiChoice(request):
    return render(request, 'lms/multi_choice.html')

def TrueFalse(request):
    return render(request, 'lms/true_false.html')

def FillBlank(request):
    return render(request, 'lms/fill_blank.html')

def Announcement(request):
    return render(request, 'lms/announcement.html')

def CourseAnnouncement(request):
    return render(request, 'lms/course_announcement.html')



# 3D Game
def Game3D(request):
    return render(request, 'lms/game.html')