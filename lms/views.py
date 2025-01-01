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

from django.db.models import Sum, F


def Login(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            return redirect('dashboard')
        else:
            return redirect('teacher_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next', 'dashboard')
            return redirect(next_url)
            # return redirect('dashboard')
        else:
            messages.error(request, 'Username or Password is incorrect')
    return render(request, 'lms/login.html', {'next': request.GET.get('next', '')})

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
    if request.user.is_teacher:
        return redirect('teacher_dashboard')
    available_courses = []

    StudentCourse = CourseToStudent.objects.filter(student_id=request.user.student_id, is_approved=True)

    for i in StudentCourse:
        get_course = Course.objects.get(course_code=i.course_code)
        available_courses.append(get_course)

    global_announcement = GlobalAnnouncement.objects.all()

    if request.method == 'POST':
        course_code = request.POST.get('course_code')
        student_id = request.user.student_id

        is_course_exist = Course.objects.filter(course_code=course_code).exists()

        if is_course_exist:
            is_exist = CourseToStudent.objects.filter(course_code=course_code, student_id=student_id).exists()

            if is_exist:
                return redirect('dashboard')
            else:
                CourseToStudent.objects.create(
                    course_code=course_code,
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

@login_required(login_url='login')
def ApplyCourse(request, course_code):
    no_student_id = False
    course_not_exist = False
    applied_successfully = False
    already_applied = False
    # is_exist = Course.objects.filter(course_code=course_code).exists()
    # is_applied = CourseToStudent.objects.filter(course_code=course_code, student_id=request.user.student_id).exists()

    # if request.user.is_student:
    #     if request.user.student_id == None:
    #         no_student_id = True
    #     else:
    #         if is_applied:
    #             if is_exist:
    #                 CourseToStudent.objects.create(
    #                     course_code=course_code, 
    #                     student_id=request.user.student_id
    #                 )
    #                 applied_successfully = True
    #             else:
    #                 course_not_exist = True
    #         else:
    #             already_applied = True
    # context = {
    #     'no_student_id': no_student_id,
    #     'course_not_exist': course_not_exist,
    #     'applied_successfully': applied_successfully,
    #     'already_applied': already_applied
    # }

    # return render(request, 'lms/student/link_page.html', context)
    if not request.user.student_id:
        no_student_id = True
        return render(request, 'lms/student/link_page.html', {
            'no_student_id': no_student_id,
        })

    # Check if the course exists
    is_exist = Course.objects.filter(course_code=course_code).exists()
    if not is_exist:
        course_not_exist = True
        return render(request, 'lms/student/link_page.html', {
            'course_not_exist': course_not_exist,
        })

    # Check if the student has already applied for the course
    is_applied = CourseToStudent.objects.filter(course_code=course_code, student_id=request.user.student_id).exists()
    if is_applied:
        already_applied = True
        return render(request, 'lms/student/link_page.html', {
            'already_applied': already_applied,
        })

    # If everything is okay, apply the student to the course
    CourseToStudent.objects.create(course_code=course_code, student_id=request.user.student_id)
    applied_successfully = True

    return render(request, 'lms/student/link_page.html', {
        'applied_successfully': applied_successfully,
    })

def Modules(request, course_code):
    course = Course.objects.get(course_code=course_code)
    modules = CourseModule.objects.filter(course=course)

    context = {
        'modules': modules
    }

    return render(request, 'lms/student/modules.html', context)

@login_required(login_url='login')
def Profile(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if request.user.is_student:
                return redirect('dashboard')
            else:
                return redirect('teacher_dashboard')
    else:
        form = CustomUserForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'lms/profile.html', context)

@login_required(login_url='login')
def CourseDetail(request, course_code):
    course = Course.objects.get(course_code=course_code)
    Announcement = CourseAnnouncement.objects.filter(course=course)

    context = {
        'announcements': Announcement,
        'course': course
    }
    return render(request, 'lms/student/course_detail.html', context)

@login_required(login_url='login')
def ModuleDetail(request):
    return render(request, 'lms/module_detail.html')

@login_required(login_url='login')
def Quizes(request, course_code):
    course = Course.objects.get(course_code=course_code)
    modules = Quiz.objects.filter(course=course).exclude(resultsquiz__student_id=request.user.student_id)

    context = {
        'quiz': modules
    }
    return render(request, 'lms/student/quizes.html', context)

@login_required(login_url='login')
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


@login_required(login_url='login')
def SubmitQuiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        correct_answers = 0
        total_questions = quiz.multiple_choice

        # Retrieve question IDs from session
        question_ids = request.session.get('multiplequestions_ids', [])
        questions = MultipleChoice.objects.filter(id__in=question_ids)

        # Check each submitted answer
        for question in questions:
            user_answer = request.POST.get(f'answer_{question.id}')
            print(f'Question {question.id}: {question.question} - User Answer: {user_answer} - Correct Answer: {question.answer}')
            if user_answer == question.answer:
                correct_answers += 1

        # Calculate score as a percentage
        score = (correct_answers / total_questions) * 100
        earn_points = round(correct_answers * 0.5)
        user = request.user
        user.total_points += earn_points
        user.save()
        
        # Save the result
        ResultsQuiz.objects.create(
            student_id=request.user.student_id,
            quiz=quiz,
            score=earn_points,
            correct_answers=correct_answers,
            course_code=quiz.course.course_code
        )
        
        return render(request, 'lms/student/quiz_results.html', {'quiz': quiz, 'score': score, 'earn_points': earn_points})

    return redirect('quiz_detail', quiz_id=quiz_id)

@login_required(login_url='login')
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



ROOMS2 = [
    (105, 'https://prod.spline.design/uDxyYJtrbVh0ylgM/scene.splinecode'),  # Basic Room
    (110, 'https://prod.spline.design/I9FQq9z3rGOsmRIu/scene.splinecode'),  # Only the PC
    (120, 'https://prod.spline.design/5scUgBZMtYVYaLf5/scene.splinecode'),  # No Music Box
    (130, 'https://prod.spline.design/B4g31xStfGKK4Hf4/scene.splinecode'),  # No Wall Deco
    (140, 'https://prod.spline.design/7Umbii56CzIoUrm3/scene.splinecode'),  # No Trash and Speaker
    (150, 'https://prod.spline.design/h02X43pscxz1snxJ/scene.splinecode'),  # No Floor Deco
    (160, 'https://prod.spline.design/s9S2Y8hx5jj4n7eI/scene.splinecode'),  # No Guitar
    (170, 'https://prod.spline.design/GfaktHDvHB-TUCEH/scene.splinecode'),  # No Chair Room
    (180, 'https://prod.spline.design/BzZsVF4PHfrGp56a/scene.splinecode'),  # No Lamp Room
    (190, 'https://prod.spline.design/a-y4N5U38kxq-0t3/scene.splinecode')   # Finish Room
]



# 3D Game
@login_required(login_url='login')
def Game3D(request):
    total_points = request.user.total_points

    all_rooms = ROOMS + ROOMS2

    # Determine the room to display based on total points
    room_url = ROOMS[0][1]  # Default to Basic Room
    for points, url in all_rooms:
        if total_points >= points:
            room_url = url

    context = {
        'room_url': room_url,
        'total_points': total_points
    }
    return render(request, 'lms/3d/game.html', context)

# Teacher
@login_required(login_url='login')
def TeacherDashboard(request):
    user = CustomUser.objects.get(id=request.user.id)
    teacher_courses = Course.objects.filter(created_by=user)
    
    for course in teacher_courses:
        course.apply_link = generate_apply_course_link(course.course_code)

    context = {
        'courses': teacher_courses,

    }
    return render(request, 'lms/teacher/dashboard.html', context)


@login_required(login_url='login')
def TeacherProfile(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if request.user.is_student:
                return redirect('dashboard')
            else:
                return redirect('teacher_dashboard')
    else:
        form = CustomUserForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'lms/teacher/profile.html', context)

@login_required(login_url='login')
def TeacherCourseDetail(request, course_code):
    course = Course.objects.get(course_code=course_code)
    Announcement = CourseAnnouncement.objects.filter(course=course)

    context = {
        'announcements': Announcement,
        'course': course
    }
    return render(request, 'lms/teacher/course_detail.html', context)

@login_required(login_url='login')
def TeacherModules(request, course_code):
    course = Course.objects.get(course_code=course_code)
    modules = CourseModule.objects.filter(course=course)

    context = {
        'modules': modules,
        'course_code': course.course_code
    }

    return render(request, 'lms/teacher/modules.html', context)

@login_required(login_url='login')
def LockModule(request, module_id):
    module = CourseModule.objects.get(id=module_id)
    module.is_active = False
    module.save()
    return redirect('teacher_modules', course_code=module.course.course_code)

def UnlockModule(request, module_id):
    module = CourseModule.objects.get(id=module_id)
    module.is_active = True
    module.save()
    return redirect('teacher_modules', course_code=module.course.course_code)


@login_required(login_url='login')
def AddModule(request, course_code):
    course = Course.objects.get(course_code=course_code)
    if request.method == 'POST':
        form = ModuleForm(request.POST, request.FILES)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            return redirect('teacher_modules', course_code=course_code)
    else:
        form = ModuleForm()
    context = {
        'form': form
    }
    return render(request, 'lms/teacher/add_module.html', context)

@login_required(login_url='login')
def TeacherQuizes(request, course_code):
    course = Course.objects.get(course_code=course_code)
    modules = Quiz.objects.filter(course=course)

    context = {
        'quiz': modules,
        'course_code': course.course_code
    }
    return render(request, 'lms/teacher/quiz.html', context)

def DeleteQuiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    quiz.delete()
    return redirect('teacher_quiz', course_code=quiz.course.course_code)

def LockQuiz(request, module_id):
    module = Quiz.objects.get(id=module_id)
    module.is_active = False
    module.save()
    return redirect('teacher_quiz', course_code=module.course.course_code)

def UnlockQuiz(request, module_id):
    module = Quiz.objects.get(id=module_id)
    module.is_active = True
    module.save()
    return redirect('teacher_quiz', course_code=module.course.course_code)

@login_required(login_url='login')
def CreateQuiz(request, course_code):
    course = Course.objects.get(course_code=course_code)
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            return redirect('teacher_quiz', course_code=course_code)
    else:
        form = QuizForm()
    context = {
        'form': form
    }
    return render(request, 'lms/teacher/add_quiz.html', context)

@login_required(login_url='login')
def TeacherCoursesAnnouncement(request, course_code):
    course = Course.objects.get(course_code=course_code)
    announcement = CourseAnnouncement.objects.filter(course=course)

    context = {
        'announcements': announcement,
        'course_code': course.course_code
    }

    return render(request, 'lms/teacher/announcements.html', context)

@login_required(login_url='login')
def CreateAnnouncement(request, course_code):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        course = Course.objects.get(course_code=course_code)
        CourseAnnouncement.objects.create(
            title=title,
            description=description,
            course=course
        )
        return redirect('course_announcement', course_code=course_code)
    return render(request, 'lms/teacher/create_announcement.html')

def DeleteAnnouncement(request, announcement_id):
    announcement = CourseAnnouncement.objects.get(id=announcement_id)
    course_code = announcement.course.course_code
    announcement.delete()
    return redirect('course_announcement', course_code=course_code)


@login_required(login_url='login')
def ListStudents(request, course_code):
    students_not_approved_ids = CourseToStudent.objects.filter(course_code=course_code, is_approved=True).values_list('student_id', flat=True)

    # Get details of those students from the Student model
    students_details = CustomUser.objects.filter(student_id__in=students_not_approved_ids)
    context = {
        'students': students_details,
        'course_code': course_code
    }
    return render(request, 'lms/teacher/list_students.html', context)

@login_required(login_url='login')
def PendingStudents(request, course_code):
    students_not_approved_ids = CourseToStudent.objects.filter(course_code=course_code, is_approved=False).values_list('student_id', flat=True)

    # Get details of those students from the Student model
    students_details = CustomUser.objects.filter(student_id__in=students_not_approved_ids)
    context = {
        'students': students_details,
        'course_code': course_code
    }
    return render(request, 'lms/teacher/pending_students.html', context)

def ApproveStudent(request, course_code, student_id):
    CourseToStudent.objects.filter(course_code=course_code, student_id=student_id).update(is_approved=True)
    return redirect('pending_students', course_code=course_code)

@login_required(login_url='login')
def Leaderboard(request, course_code):
    leaderboard = (
        ResultsQuiz.objects.filter(course_code=course_code)
        .values('student_id')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')
    )

    leaderboard_with_details = []
    for result in leaderboard:
        student_details = CustomUser.objects.filter(student_id=result['student_id']).first()
        if student_details:
            leaderboard_with_details.append({
                'student_id': result['student_id'],
                'first_name': student_details.first_name,
                'last_name': student_details.last_name,
                'total_score': result['total_score']
            })

    context = {
        'students': leaderboard_with_details
    }
    
    return render(request, 'lms/teacher/leaderboard_view.html', context)

@login_required(login_url='login')
def StudentLeaderboard(request, course_code):
    student_id = request.user.student_id
    
    # Step 1: Get the leaderboard with ranks
    leaderboard = (
        ResultsQuiz.objects.filter(course_code=course_code)
        .values('student_id')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')
    )
    
    # Step 2: Build the leaderboard with details and find the student's rank
    leaderboard_with_details = []
    student_rank = None
    student_score = 0

    for rank, result in enumerate(leaderboard, start=1):
        student_details = CustomUser.objects.filter(student_id=result['student_id']).first()
        if student_details:
            # Add the student's details and rank to the leaderboard
            leaderboard_with_details.append({
                'rank': rank,
                'student_id': result['student_id'],
                'first_name': student_details.first_name,
                'last_name': student_details.last_name,
                'email': student_details.email,
                'total_score': result['total_score']
            })

            # Check if this is the logged-in student
            if result['student_id'] == student_id:
                student_rank = rank
                student_score = result['total_score']

    # Return the leaderboard along with the logged-in student's rank and score
    context = {
        'students': leaderboard_with_details,
        'student_rank': student_rank,
        'student_score': student_score
    }
    return render(request, 'lms/student/leaderboard_view.html', context)


def AssetLink(request):
    assetlink = [
        {
            "relation": ["delegate_permission/common.handle_all_urls"],
            "target": {
            "namespace": "android_app",
            "package_name": "xyz.appmaker.yiwvwg",
            "sha256_cert_fingerprints": ["75:44:B1:7B:3C:AA:A1:67:DC:44:B8:F5:6B:F6:D6:2D:10:4C:7F:20:BC:05:E2:FC:44:96:22:07:AD:1F:A6:6B"]
            }
        }
    ]

    return JsonResponse(assetlink, safe=False)

def generate_apply_course_link(course_code):
    base_url = "https://techknow.ellequin.com/"
    return f"{base_url}apply_course/{course_code}"



def test_game(request, room_number):
    room_number = int(room_number)
    if room_number == 1:
        room_url = 'https://prod.spline.design/a7GTFzRLRz6DkNfd/scene.splinecode'
    elif room_number == 2:
        room_url = 'https://prod.spline.design/a-y4N5U38kxq-0t3/scene.splinecode'
    
    context = {
        'room_url': room_url
    }
    return render(request, 'lms/3d/dashboard-test.html', context)


def preview_game(request):
    return render(request, 'lms/student/room_preview.html')


def admin_dashboard(request):
    return render(request, 'lms/admin_side/admin_dashboard.html')