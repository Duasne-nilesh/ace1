from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
from django import forms
from datetime import datetime, timedelta
from pprint import pprint

class extendUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    m_num = models.BigIntegerField()
    year = models.CharField(max_length=50)
    s_id = models.BigIntegerField()
    dpt = models.CharField(max_length=50)
    def __str__(self):
        return self.user.first_name

class year(models.Model):
    yr = models.CharField(max_length=100)
    def __str__(self):
        return self.yr

class semester(models.Model):
    year = models.ForeignKey(year, on_delete=models.CASCADE)
    sem = models.CharField(max_length=50)
    def __str__(self):
        return self.sem

