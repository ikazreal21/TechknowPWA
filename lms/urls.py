from django.contrib.auth import views as auth_views
from django.urls import re_path as url

from django.urls import path
from . import views

from pwa.views import manifest, service_worker, offline



urlpatterns = [
    path("", views.Dashboard, name="dashboard"),
    # path("dashboard/", views.Dashboard, name="dashboard"),
    path("courses/", views.Courses, name="courses"),
    path("course_details/<str:course_code>", views.CourseDetail, name="course_details"),
    path("modules/<str:course_code>", views.Modules, name="modules"),
    path("quiz/<str:course_code>", views.Quizes, name="quiz"),
    path("pastquiz/", views.PastQuizzes, name="pastquiz"),
    path("quiz_detail/<str:quiz_id>", views.MultiChoice, name="quiz_detail"),
    path("submit_quiz/<str:quiz_id>", views.SubmitQuiz, name="submit_quiz"),
    path("profile/", views.Profile, name="profile"),
    path("course_detail/", views.CourseDetail, name="course_detail"),
    path("module_detail/", views.ModuleDetail, name="module_detail"),


    # 3D Game
    path("3d_game/", views.Game3D, name="3d_game"),
    

    # Teacher
    path("teacher/", views.TeacherDashboard, name="teacher_dashboard"),
    # path("teacher/courses/", views.TeacherCourses, name="teacher_courses"),
    path("teacher/course_detail/<str:course_code>", views.TeacherCourseDetail, name="teacher_course_detail"),

    path("teacher/modules/<str:course_code>", views.TeacherModules, name="teacher_modules"),
    path("lock_module/<str:module_id>", views.LockModule, name="lock_module"),
    path("unlock_module/<str:module_id>", views.UnlockModule, name="unlock_module"),
    path("add_module/<str:course_code>", views.AddModule, name="add_module"),

    path("teacher/quiz/<str:course_code>", views.TeacherQuizes, name="teacher_quiz"),
    path("lock_quiz/<str:module_id>", views.LockQuiz, name="lock_quiz"),
    path("unlock_quiz/<str:module_id>", views.UnlockQuiz, name="unlock_quiz"),
    path("create_quiz/<str:course_code>", views.CreateQuiz, name="create_quiz"),
    path("delete_quiz/<str:quiz_id>", views.DeleteQuiz, name="delete_quiz"),

    path("course_announcement/<str:course_code>", views.TeacherCoursesAnnouncement, name="course_announcement"),
    path("create_announcement/<str:course_code>", views.CreateAnnouncement, name="create_announcement"),
    path("delete_announcement/<str:announcement_id>", views.DeleteAnnouncement, name="delete_announcement"),

    path("list_students/<str:course_code>", views.ListStudents, name="list_students"),
    path("pending_students/<str:course_code>", views.PendingStudents, name="pending_students"),
    path("approve_student/<str:course_code>/<str:student_id>", views.ApproveStudent, name="approve_student"),

    path("leaderboard/<str:course_code>", views.Leaderboard, name="leaderboard"),
    path("studentleaderboard/<str:course_code>", views.StudentLeaderboard, name="studentleaderboard"),

    path("apply_course/<str:course_code>", views.ApplyCourse, name="apply_course"),

    # path("create_module/<str:course_code>", views.CreateModule, name="create_module"),
    # path("create_course/", views.CreateCourse, name="create_course"),
    # path("teacher/quiz_results/<str:quiz_id>", views.QuizResults, name="quiz_results"),
    path("teacherprofile/", views.TeacherProfile, name="teacher_profile"),

    path("test_game/<str:room_number>", views.test_game, name="test_game"),
    path("preview_game/", views.preview_game, name="preview_game"),


    # Auth
    path("login/", views.Login, name="login"),
    path("register/", views.Register, name="register"),
    path("logout/", views.Logout, name="logout"),

    # pwa
    url(r'^serviceworker\.js$', service_worker, name='serviceworker'),
    url(r'^manifest\.json$', manifest, name='manifest'),
    url('^offline/$', offline, name='offline'),

    path(".well-known/assetlinks.json", views.AssetLink),
]



    