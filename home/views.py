from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from login.models import student, teacher, Subject, Attendance
from django.http import HttpResponse
from django.contrib.auth import logout
# Create your views here.
@login_required
def home(request):
    return render(request, 'home.html')
@login_required
def profile(request):
    if not request.user.is_staff:
        stdnt = student.objects.get(username=request.user.username)
        context = {
            'name': stdnt.name,
            'address': stdnt.address,
            'contact': stdnt.phoneNO,
            'gender': stdnt.gender,
            'email': stdnt.email,
            'img': stdnt.image,
            'roll': stdnt.roll_no,
            'course': stdnt.course,
            'sem': stdnt.semester,
            'dob': stdnt.date_of_birth,
            'teacher': False
        }
        return render(request, 'profile.html', context)
    else:
        try:
            tech = teacher.objects.get(username=request.user.username)
        except:
            return HttpResponse('<h3>current staff account dont have teacher profile </h3><h4>Ask administrator for teacher account</h4>')
        context = {
            'name': tech.name,
            'address': tech.address,
            'contact': tech.phoneNO,
            'gender': tech.gender,
            'email': tech.email,
            'img': tech.image,
            'dob': tech.date_of_birth,
            'subjects': tech.subjects,
            'teacher': True
        }
        return render(request, 'profile.html', context)
@login_required
def academic(request):
    if not request.user.is_staff:
        stdnt = student.objects.get(username=request.user.username)
        subjects = Subject.objects.filter(course=stdnt.course, semester=stdnt.semester)
        context = {
            'course': stdnt.course,
            'subjects': subjects
        }
        return render(request, 'academic.html', context)
    else:
        try:
            tech = teacher.objects.get(username=request.user.username)
        except:
            return HttpResponse('<h1>This staff acount dont have associated subjects</h1>')
        context={
            'teacher': True,
            'subjects': tech.subjects
        }
        return render(request, 'academic.html', context)
@login_required
def attendence(request):
    if not request.user.is_staff:
        if request.method == 'POST':
            date = request.POST['date']
            stdnt = student.objects.get(username=request.user.username)
            subjects_all = Subject.objects.filter(course=stdnt.course, semester=stdnt.semester)
            statuss =[]
            for i in subjects_all:
                status = Attendance.objects.filter(semester=stdnt.semester, subject=i, roll_no=stdnt.roll_no, date=date)
                statuss.append((i,status))
            context = {
                'date': date,
                'status': statuss,
                'processed': True,
            }
            return render(request, 'attendence.html', context)
                
        return render(request, 'attendence.html')

@login_required
def log_out(request):
    logout(request)
    return redirect('home:home')