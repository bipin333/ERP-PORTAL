from django.contrib import admin

# Register your models here.
from .models import student,teacher,Attendance,Subject,Files, Result, Mark
admin.site.register(student)
admin.site.register(teacher)
admin.site.register(Attendance)
admin.site.register(Subject)
admin.site.register(Files)
admin.site.register(Result)
admin.site.register(Mark)