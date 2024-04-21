from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
#Note all null=True are only for testing purpose
class Files(models.Model):
    file = models.FileField(upload_to='study_materials')
    name = models.CharField(max_length=20, null=True)
    def __str__(self):
        return self.name
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
    name = models.CharField(max_length=30, unique=True)
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
        return self.roll_no + ' ' + self.subject.name + ' ' + self.date.isoformat()

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

class Mark(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    mark = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    session = models.CharField(max_length=10, choices=[('mst-1', 'sessional 2'), ('mst-2', 'sessional 1'), ('final', 'Final')],null=True)
    def __str__(self):
        return f'{self.student.name} - {self.subject.name} - {self.mark}'
    class Meta:
        unique_together = (('student', 'subject', 'session'),)
    @staticmethod
    def get_percentage(stdnt, session):
        all_marks = Mark.objects.filter(student=stdnt, session=session)
        total_marks = 0
        for mark in all_marks:
            total_marks += mark.mark
        if not all_marks or total_marks == 0:
            return 0
        return round((total_marks / (len(all_marks)*100)) * 100, 2)