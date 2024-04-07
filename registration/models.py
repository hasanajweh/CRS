from django.db import models
from django.conf import settings



class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    instructor = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()


    def __str__(self):
        return f"{self.code} - {self.name}"

class CourseSchedule(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    days = models.CharField(max_length=50)  # Sunday, Monday, Tuesday, etc.
    startTime = models.TimeField()
    endTime = models.TimeField()
    roomNo = models.CharField(max_length=20)

class StudentRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

 

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Add additional fields here
    pass



