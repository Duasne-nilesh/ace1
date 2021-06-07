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
    done = quiz_response.objects.order_by().filter(student_id=request.user.id).values('subject','year','semester').distinct().values('subject')
    for d in done:
        print(d)
    inf = extendUser.objects.filter(user=request.user.id).first()
    print(inf.year)
    a = questions.objects.order_by().filter(year=inf.year).values('subject','year','semester').distinct().exclude(subject__in=done)
    return render(request,'exam.html',{'a':a,'inf':inf})

def start_exam(request,subject):
    if request.user.is_authenticated:
        if request.method == "POST":
            array_data = request.POST['submission']
            data = json.loads(array_data)
            print(data)
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
            # return redirect('/report_details/'+subject)
        que = questions.objects.filter(subject=subject)
        for q in que:
            print(q.year)
        return render(request,'start_exam.html',{'que':que,'subject':subject})



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
    return render(request,'view_question.html',{'query':query,'subject':subject})

@staff_member_required
def delete_test(request,subject):
    delqueries = questions.objects.filter(subject=subject).delete()
    return redirect('/faculty')

def view_report(request):
    a = quiz_response.objects.filter(student_id=request.user.id).order_by().values('subject','year','semester').distinct()
    return render(request,'view_report.html',{'a':a})

def report_details(request,subject):
    # print(subject)
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
    return render(request,'view_report_details.html',{'subject':subject,'total':total,'total_marks':total_marks,'k':k,'k_c':k_c,'a':a,'a_c':a_c,'app':app,'app_c':app_c,'u':u,'u_c':u_c})
