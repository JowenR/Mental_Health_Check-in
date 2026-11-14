from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

class Student(User):
    class Meta:
        proxy = True
        verbose_name = "Student"
        verbose_name_plural = "Students"


class AdminAccount(User):
    class Meta:
        proxy = True
        verbose_name = "Admin"
        verbose_name_plural = "Admins"
class CounselorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="counselor_profile",
    )
    specialization = models.CharField(max_length=120, blank=True)
    office_location = models.CharField(max_length=120, blank=True)
    contact_number = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"Counselor profile for {self.user.username}"


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    course = models.CharField(max_length=120, blank=True)
    year_level = models.CharField(max_length=30, blank=True)
    contact_number = models.CharField(max_length=30, blank=True)
    facebook_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f"Student profile for {self.user.username}"