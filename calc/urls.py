from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    # path('faculty',views.faculty,name='faculty'),
    path('create_exam',views.create_exam,name='create_exam'),
    path('post',views.post,name='post'),
    path('report',views.report,name='report'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('setq',views.setq,name='setq'),
    path('index',views.index,name='index'),
    path('profile',views.profile,name='profile'),

    
]