from django.contrib.auth import views as auth_views

from django.urls import path
from . import views




urlpatterns = [
    path("", views.Dashboard, name="dashboard"),
    path("dashboard/", views.Dashboard, name="dashboard"),
    path("courses/", views.Courses, name="courses"),
    path("apply_course/", views.ApplyCourse, name="apply_course"),
    path("modules/", views.Modules, name="modules"),
    path("profile/", views.Profile, name="profile"),
    path("course_detail/", views.CourseDetail, name="course_detail"),
    path("module_detail/", views.ModuleDetail, name="module_detail"),
    path("quiz/", views.Quiz, name="quiz"),
    path("quiz_result/", views.QuizResult, name="quiz_result"),\
    path("announcement/", views.Announcement, name="announcement"),
    path("course_announcement/", views.CourseAnnouncement, name="course_announcement"),
    


    # Auth
    path("login/", views.Login, name="login"),
    path("register/", views.Register, name="register"),
    path("logout/", views.Logout, name="logout"),
]



    