from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from login.models import student, teacher, Subject, Attendance, Files, Mark
from django.http import HttpResponse
from django.contrib.auth import logout
import datetime
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
        if request.method == 'POST':
            file = request.FILES['file']
            subject = request.POST['subject']
            name = request.POST['name']
            file_new = Files.objects.create(name=name, file=file)
            file_new.save()
            sub = Subject.objects.get(name=subject)
            sub.materials.add(file_new)
            return HttpResponse('Sucess')
        else:
            try:
                tech = teacher.objects.get(username=request.user.username)
            except:
                return HttpResponse('<h1>This staff acount dont have associated subjects</h1>')
            context={
                'teacher': True,
                'subjects': tech.subjects.all()
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
                'student': True,
            }
            return render(request, 'attendence.html', context)
        context = {
            'student': True
        }
        return render(request, 'attendence.html',context)
    else:
        tech = teacher.objects.get(username=request.user.username)
        subjects_all = tech.subjects.all()
        if request.method == 'POST':
            if 'subject-select' in request.POST:
                sub = request.POST['sub']
                sem = Subject.objects.filter(name=sub)
                sem = sem[0].semester
                students_all = student.objects.filter(semester=sem).order_by('roll_no')
                subject = Subject.objects.filter(name=sub)
                subject = subject[0]
                attendence_already_present = Attendance.objects.filter(subject=subject,date=datetime.date.today())
                if attendence_already_present:
                    return HttpResponse('Attendence for today already upladed')
                else:
                    context = {
                        'subject' : sub,
                        'students': students_all,
                        'loaded': True,
                        'semester': sem,
                    }
                    return render(request, 'attendence.html', context)
            elif 'attendence-submit' in request.POST:
                roll_numbers = request.POST.getlist('roll_no')
                semester = request.POST['semester']
                subject = request.POST['subject']
                subject = Subject.objects.filter(name=subject)
                for roll in roll_numbers:
                    status = request.POST.get(roll) == 'on'
                    at = Attendance(
                        roll_no=roll,
                        subject=subject[0],
                        date = datetime.date.today(),
                        semester = semester,
                        status = status
                    )
                    at.save()
                return HttpResponse('attendence send to server')
        else:
            context = {
                'subject' : subjects_all
            }
            return render(request, 'attendence.html', context)
@login_required
def result(request):
    if not request.user.is_staff:
        if request.method == 'POST':
            session = request.POST['session']
            stdnt = student.objects.filter(username=request.user.username)
            marks = Mark.objects.filter(student=stdnt[0],session=session)
            context={
                'data':marks,
                'percentage': Mark.get_percentage(stdnt[0],session),
            }
            return render(request, 'result.html', context)
        return render(request, 'result.html')
    else:
        tech = teacher.objects.get(username=request.user.username)
        if request.method == 'POST':
            if 'step-1' in request.POST:
                sub = request.POST['subject']
                subject = Subject.objects.filter(name=sub)
                sem = subject[0].semester
                student_all = student.objects.filter(semester=sem)
                context = {
                    'students': student_all.all(),
                    'subject':sub,
                    'step2': True,
                    'teacher': True,
                }
                return render(request, 'result.html', context)
            elif 'step-2' in request.POST:
                sub = request.POST['subject']
                session = request.POST['session']
                subject = Subject.objects.filter(name=sub)
                students = request.POST.getlist('roll_no')
                for stdnt in students:
                    mrk = request.POST.get(stdnt)
                    stdnt_object = student.objects.filter(roll_no=stdnt)
                    mt = Mark(
                        student=stdnt_object[0],
                        subject=subject[0],
                        mark=mrk,
                        session = session
                    )
                    mt.save()
                return HttpResponse('marks uploaded')
                    
        context = {
            'subjects': tech.subjects.all(),
            'teacher': True,
            'step1': True,
        }
        return render(request,'result.html',context)
@login_required
def log_out(request):
    logout(request)
    return redirect('home:home')