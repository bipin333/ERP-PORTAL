from django.db import models

# Create your models here.

class student(models.Model):
    username = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=30, null=True)
    phoneNO = models.CharField(max_length=10, null=True)
    email = models.CharField(max_length=30, null=True)
    image = models.ImageField(upload_to='student_images', null=True)
    roll_no = models.CharField(max_length=10, null=True)
    COURSE_CHOICES = [
        ('BTech CSE', 'BTech Computer Science & Engineering'),
        ('Civil', 'Civil Engineering'),
        ('Law', 'Law'),
    ]
    course = models.CharField(max_length=20, choices=COURSE_CHOICES, null=True)
    date_of_birth = models.DateField(null=True)

    def __str__(self):
        return self.name