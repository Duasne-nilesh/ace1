from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
from django import forms
from datetime import datetime, timedelta
from pprint import pprint

class questions(models.Model):
    year = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    question = models.CharField(max_length=900)
    option1 = models.CharField(max_length=800)
    option2 = models.CharField(max_length=800)
    option3 = models.CharField(max_length=800)
    option4 = models.CharField(max_length=800)
    answer = models.CharField(max_length=800)
    category = models.CharField(max_length=400)

class quiz_response(models.Model):
    student_id = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    q_id = models.CharField(max_length=900)
    sub_answer = models.CharField(max_length=800)
    corr_answer = models.CharField(max_length=800)
    marks = models.CharField(max_length=800)
    category = models.CharField(max_length=400)

