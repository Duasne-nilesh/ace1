from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required


def home(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("/index")
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/')
    else:    
        return render(request,'login.html')


def index(request):
    return render(request,'student/index.html')
@staff_member_required
def create_class(request):
    return render(request,'create_class.html')
@staff_member_required
def setq(request):
    return render(request,'set_q.html')
@staff_member_required
def create_exam(request):
        return render(request,'create_exam.html')
@staff_member_required
def post(request):
    return render(request,'post.html')
@staff_member_required
def report(request):
    return render(request,'report.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        input_password = request.POST['input_password']
        email = request.POST['email']
        if request.POST['input_password']==request.POST['confirm_password']:
            try:
                user = User.objects.get(username=request.POST['email'])
                return render(request, 'register.html',{'error':"Email is already taken"})
            except User.DoesNotExist:
                user = User.objects.create_user(username=email,password=input_password,first_name=first_name,last_name=last_name)
                year = request.POST['year']
                s_id = request.POST['s_id']
                m_num = request.POST['m_num']
                dpt = request.POST['dpt']
                ext = extendUser(year=year,s_id=s_id,m_num=m_num,user=user,dpt=dpt)
                ext.save();
                return redirect('/')
        else:
            messages.info(request,'password not matching')
            return redirect('register')
        return redirect('/')
    else:
        return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def profile(request):
    inf = extendUser.objects.filter(user=request.user.id)
    return render(request,'student/profile.html',{'inf':inf});



