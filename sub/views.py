from django.shortcuts import render, redirect
from django.http import HttpResponse, response
from requests.api import request
from .models import *
from calc.models import *
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
import requests
import json


def exams(request):
    a = questions.objects.order_by().values('subject','year','semester').distinct()
    inf = extendUser.objects.filter(user=request.user.id)
    return render(request,'student/exam.html',{'a':a,'inf':inf})

def start_exam(request,subject):
    if request.user.is_authenticated:
        if request.method == "POST":
            array_data = request.POST['submission']
            data = json.loads(array_data)
            for obj in data:
                vals = list(obj.values())
                print(vals)
                year = vals[0]
                sem = vals[1]
                subject = vals[2]
                q_id = int(vals[3])
                sub_answer = vals[4]
                corr_answer = vals[5]
                category = vals[6]
                marks=0
                if sub_answer == corr_answer:
                    marks = 1
                else:
                    marks = 0
                print(marks)
                res = quiz_response(student_id=request.user.id,year=year, semester=sem,subject=subject,q_id=q_id,sub_answer=sub_answer,corr_answer=corr_answer,category=category,marks=marks)
                res.save()
                return redirect('student/report_details/'+subject)
        que = questions.objects.filter(subject=subject)
        return render(request,'student/start_exam.html',{'que':que,'subject':subject})

def submit_response(request):
    pass
    # print(json.loads(request.POST.get('data', ''))
    # return render(request,'student/start_exam.html')



@staff_member_required
def setexam(request):
    if request.method == "POST":
        year = request.POST['year']
        semester = request.POST['semester']
        subject = request.POST['subject']
    return render(request,'sub/ffem.html',{'year':year,'semester':semester,'subject':subject})
@staff_member_required
def ffem(request):
    if request.method == "POST":
        year = request.GET['year']
        semester = request.GET['semester']
        subject = request.GET['subject'] 
        question = request.POST['question']  
        option1 = request.POST['option1']
        option2 = request.POST['option2']
        option3 = request.POST['option3']
        option4 = request.POST['option4']
        answer = request.POST['answer']
        response = requests.post("http://localhost:5000/predict_api",data={'question':question}).json()
        print(response)
        category = response['label']
        print(category)
        fa = questions(year=year,semester=semester,subject=subject,question=question,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer,category=category)
        fa.save()
    return render(request,'sub/ffem.html',{'year':year,'semester':semester,'subject':subject,'category':category})

@staff_member_required
def faculty(request):
    query = questions.objects.order_by().values('subject','year','semester').distinct()
    return render(request,'faculty.html',{'query': query})

@staff_member_required
def view_question(request,subject):
    query = questions.objects.filter(subject=subject)
    return render(request,'view_question.html',{'query':query})

@staff_member_required
def delete_test(request,subject):
    delqueries = questions.objects.filter(subject=subject).delete()
    return redirect('/faculty')

def view_report(request):
    a = questions.objects.order_by().values('subject','year','semester').distinct()
    return render(request,'view_report.html',{'a':a})

def report_details(request,subject):
    print(subject)
    full_data = quiz_response.objects.filter(student_id=request.user.id,subject=subject)
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
        if data.category=="Knowledge":
            k+=1
            if data.marks == 1:
                k_c+=1
                total_marks+=1
            
        if data.category=="Understanding":
            u+=1
            if data.marks == 1:
                u_c+=1
                total_marks+=1
            
        if data.category=="Application":
            app+=1
            if data.marks == 1:
                app_c+=1
                total_marks+=1
            
        if data.category=="Analysis":
            a+=1
            if data.marks == 1:
                a_c+=1
                total_marks+=1
            

    return render(request,'view_report_details.html',{'total':total,'marks':total_marks,'k':k,'k_c':k_c})
