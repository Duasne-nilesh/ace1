from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from sub.models import *
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count,Sum
from django.contrib.auth.models import User

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
    return redirect('exams')
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
    a = quiz_response.objects.order_by().values('subject','year','semester').distinct()
    return render(request,'report.html',{'a':a})

@staff_member_required
def performance(request,subject):
    full_data = quiz_response.objects.filter(subject=subject)
    rows = quiz_response.objects.filter(subject=subject).values('student_id').annotate(score=Sum('marks'),total=Count('marks'))
    res = []
    for row in rows:
        print(row['student_id'])
        user = User.objects.filter(id=row['student_id']).values('first_name','last_name').first()
        dict = {'Name':user['first_name'] + " " + user['last_name'],'score':int(row['score']),'total':row['total']}
        res.append(dict)
    print(res)
    total=0
    total_marks = 0
    k=0
    k_c=0
    u=0
    u_c=0
    a=0
    a_c=0
    app=0
    app_c=0
    for data in full_data:
        total+=1
        # print(data.marks)
        if data.category=="Knowledge":
            k+=1
            if int(data.marks) == 1:
                k_c+=1
                total_marks+=1
            
        if data.category=="Understanding":
            u+=1
            if int(data.marks) == 1:
                u_c+=1
                total_marks+=1
            
        if data.category=="Application":
            app+=1
            if int(data.marks) == 1:
                app_c+=1
                total_marks+=1
            
        if data.category=="Analysis":
            a+=1
            if int(data.marks) == 1:
                a_c+=1
                total_marks+=1
            
    print(total)
    print(total_marks)
    return render(request,'performance.html',{'data':res,'subject':subject,'total':100,'total_marks':round(total_marks/total*100, 2),'k':100,'k_c':round(k_c/k*100,2),'a':100,'a_c':round(a_c/a*100,2),'app':100,'app_c':round(app_c/app*100,2),'u':100,'u_c':round(u_c/u*100,2)})

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
    return render(request,'profile.html',{'inf':inf});



