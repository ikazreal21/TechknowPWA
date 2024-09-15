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
    return render(request, 'lms/login.html')

def Register(request):
    return render(request, 'lms/register.html')

def Logout(request):
    return redirect('login')

def Dashboard(request):
    return render(request, 'lms/dashboard.html')

def Courses(request):
    return render(request, 'lms/courses.html')

def ApplyCourse(request):
    return render(request, 'lms/apply_course.html')

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

def Game(request):
    return render(request, 'lms/game.html')