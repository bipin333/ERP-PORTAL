from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages
from .models import student
# Create your views here.
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            request.session['logged_in'] = True
            return redirect('home:home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login_page.html')

def register_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return HttpResponse('UserName already exists')
        name = request.POST['name']
        address = request.POST['address']
        phone_no = request.POST['phone']
        email = request.POST['mail']
        roll_no = request.POST['roll']
        course = request.POST['course']
        date_of_birth = request.POST['dob']
        imagee = request.FILES['img']

        user = User.objects.create_user(username=username, password=password)

        stdnt = student.objects.create(
            username=username,
            password=password,
            name=name,
            address=address,
            phoneNO=phone_no,
            email=email,
            roll_no=roll_no,
            course=course,
            date_of_birth=date_of_birth,
            image = imagee
        )
        user.save()
        stdnt.save()
        
        return HttpResponse('Registration successful')
    
    return render(request, 'register_page.html')