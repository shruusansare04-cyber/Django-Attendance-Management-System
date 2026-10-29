from django.db import models
from django.contrib.auth.models import User


# =========================
# Student
# =========================

class Student(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )

    roll_no = models.IntegerField()

    email = models.EmailField()

    course = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name


# =========================
# Subject
# =========================

class Subject(models.Model):

    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=20
    )

    def __str__(self):
        return self.name


# =========================
# Teacher
# =========================

class Teacher(models.Model):

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    # Teacher can teach multiple subjects
    subjects = models.ManyToManyField(
        Subject,
        blank=True
    )

    def __str__(self):
        return self.name


# =========================
# Attendance
# =========================

class Attendance(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    status = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.student.name} - {self.date}"


# =========================
# User Profile
# =========================

class UserProfile(models.Model):

    ROLE_CHOICES = (
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("admin", "Admin"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="student"
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"