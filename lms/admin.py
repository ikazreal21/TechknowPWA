from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models
from django.contrib.auth.models import Group
from admin_interface.models import Theme

class UserAdminConfig(UserAdmin):
    model = CustomUser
    search_fields = ('username', 'email')
    list_filter = ('first_name', 'is_active', 'is_staff', 'gender', 'birth_date', 'is_teacher', 'is_student')
    list_display = ('username', 'id', 'email','is_active', 'is_staff', 'gender', 'birth_date', 'is_student', 'is_teacher', 'total_points')
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'username', 'email', 'password', 'gender', 'birth_date', 'student_id', 'total_points',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_student', 'is_teacher')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})}
    }
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'first_name', 
                    'last_name',
                    'username',
                    'email',
                    'password1',
                    'password2',
                    'gender', 
                    'birth_date',
                    'student_id',
                    'image',
                    'is_active',
                    'is_staff',
                    'is_student',
                    'is_teacher'
                ),
            },
        ),
    )

admin.site.unregister(Group)
# admin.site.unregister(Theme)
admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(Course)
admin.site.register(CourseToStudent)
admin.site.register(CourseModule)
admin.site.register(CourseAnnouncement)
admin.site.register(GlobalAnnouncement)
admin.site.register(Quiz)
admin.site.register(MultipleChoice)
admin.site.register(TrueFalse)
admin.site.register(FillInTheBlank)
admin.site.register(ResultsQuiz)
admin.site.register(ThreeDRoom)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(CoursetoProf)


admin.site.site_title = "Techknow Admin"
admin.site.site_header = "Techknow Admin"