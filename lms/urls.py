from django.contrib.auth import views as auth_views

from django.urls import path
from . import views




urlpatterns = [
    path("", views.Dashboard, name="dashboard"),
    # path("dashboard/", views.Dashboard, name="dashboard"),
    path("courses/", views.Courses, name="courses"),

    path("apply_course/<str:course_code>", views.ApplyCourse, name="apply_course"),

    path("course_details/<str:course_code>", views.CourseDetail, name="course_details"),
    
    path("modules/<str:course_code>", views.Modules, name="modules"),
         
    path("quiz/<str:course_code>", views.Quizes, name="quiz"),
    
    path("pastquiz/", views.PastQuizzes, name="pastquiz"),

    path("quiz_detail/<str:quiz_id>", views.MultiChoice, name="quiz_detail"),

    path("submit_quiz/<str:quiz_id>", views.SubmitQuiz, name="submit_quiz"),


    path("profile/", views.Profile, name="profile"),
    path("course_detail/", views.CourseDetail, name="course_detail"),
    path("module_detail/", views.ModuleDetail, name="module_detail"),
    path("quiz_result/", views.QuizResult, name="quiz_result"),\
    path("course_announcement/", views.CourseAnnouncement, name="course_announcement"),

    # 3D Game
    path("3d_game/", views.Game3D, name="3d_game"),
    


    # Auth
    path("login/", views.Login, name="login"),
    path("register/", views.Register, name="register"),
    path("logout/", views.Logout, name="logout"),
]



    