from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
#Note all null=True are only for testing purpose
class Files(models.Model):
    file = models.FileField(upload_to='study_materials')
class student(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=1, choices=[('m', 'Male'), ('f', 'Female'), ('o', 'Others')], null=True)
    phoneNO = models.CharField(max_length=10, null=True)
    email = models.CharField(max_length=30, null=True)
    image = models.ImageField(upload_to='student_images/', null=True)
    roll_no = models.CharField(max_length=10, unique=True)
    COURSE_CHOICES = [
        ('BTech CSE', 'BTech Computer Science & Engineering'),
        ('Civil', 'Civil Engineering'),
        ('Law', 'Law'),
    ]
    course = models.CharField(max_length=20, choices=COURSE_CHOICES, null=True)
    semester = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)], null=True
    )
    date_of_birth = models.DateField(null=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=30, null=True)
    course = models.CharField(max_length=20, choices=student.COURSE_CHOICES, null=True)
    semester = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)], null=True
    )
    materials = models.ManyToManyField(Files, blank=True)
    def __str__(self):
        return self.name

class Attendance(models.Model):
    roll_no = models.CharField(max_length=10, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    status = models.BooleanField(default=False)
    semester = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)], null=True
    )

    def __str__(self):
        return self.roll_no

class teacher(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=1, choices=[('m', 'Male'), ('f', 'Female'), ('o', 'Others')], null=True)
    phoneNO = models.CharField(max_length=10, null=True)
    email = models.CharField(max_length=30, null=True)
    image = models.ImageField(upload_to='teacher_images/', null=True)
    date_of_birth = models.DateField(null=True)
    subjects = models.ManyToManyField(Subject, blank=True)

    def __str__(self):
        return self.name