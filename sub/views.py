from django.shortcuts import render, redirect
from django.http import HttpResponse, response
from .models import *
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
import requests


def exam(request):
    a = questions.objects.order_by().values('subject','year','semester').distinct()
    inf = extendUser.objects.filter(user=request.user.id)
    return render(request,'student/exam.html',{'a':a,'inf':inf})

def start_exam(request,subject):
    que = questions.objects.filter(subject=subject)
    return render(request,'student/start_exam.html',{'que':que})

def submit_response(request):
    print(request)
    """return render(request,'student/start_exam.html',{'que':que})"""

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