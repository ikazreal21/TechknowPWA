from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import locale
import uuid

from django.core.files.storage import FileSystemStorage
from django.db import models
from datetime import datetime


def create_rand_id():
        from django.utils.crypto import get_random_string
        return get_random_string(length=13, 
            allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')


class CustomUser(AbstractUser):
    GENDER = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, choices=GENDER, null=True, blank=True)
    birth_date = models.CharField(max_length=50, null=True, blank=True)
    student_id = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='uploads/profile', blank=True, null=True)
    total_points = models.IntegerField(default=0)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def date(self):
        try:
            # Convert the birth_date string to a datetime object
            date_obj = datetime.strptime(self.birth_date, "%Y-%m-%d")
            # Format it to 'Month day, Year' (e.g., 'September 21, 2024')
            return date_obj.strftime("%B %d, %Y")
        except ValueError:
            return self.birth_date


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/course', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='course_created_by')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='course_updated_by')
    is_active = models.BooleanField(default=True)
    course_code = models.CharField(max_length=50, default=create_rand_id, unique=True)

    def __str__(self):
        return f"{self.name}"

class CourseToStudent(models.Model):
    course_code = models.CharField(max_length=50, null=True, blank=True)
    student_id = models.CharField(max_length=50, null=True, blank=True)
    points = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_code} - {self.student_id} - {self.is_approved} - {self.created_at}"
    

class CourseModule(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    module_file = models.FileField(upload_to='uploads/module', blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"
    
class GlobalAnnouncement(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        ordering = ['-created_at']
    
class CourseAnnouncement(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
    

class MultipleChoice(models.Model):
    question = models.TextField()
    option1 = models.CharField(max_length=50)
    option2 = models.CharField(max_length=50)
    option3 = models.CharField(max_length=50)
    option4 = models.CharField(max_length=50)
    answer = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question}"

class TrueFalse(models.Model):
    question = models.TextField()
    answer = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question}"

class FillInTheBlank(models.Model):
    question = models.TextField()
    answer = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question}"

class Quiz(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    multiple_choice = models.IntegerField(default=0)
    true_false = models.IntegerField(default=0)
    fill_in_the_blank = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"
    
    def total_questions(self):
        return self.multiple_choice + self.true_false + self.fill_in_the_blank
    
    class Meta:
        verbose_name_plural = "Quizzes"
    
class ResultsQuiz(models.Model):
    student_id = models.CharField(max_length=50)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    course_code = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id} - {self.quiz} - {self.score}"
    
# class GameCharacter(models.Model):
#     name = models.CharField(max_length=50)
#     image = models.ImageField(upload_to='uploads/character', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='game_character_created_by')

#     def __str__(self):
#         return f"{self.name}"
    class Meta:
        verbose_name_plural = "Results Quizzes"

class ThreeDRoom(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads/3droom', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"