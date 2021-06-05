from django.urls import path
from . import views

urlpatterns = [
    path('setexam',views.setexam,name='setexam'),
    path('faculty',views.faculty,name='faculty'),
    path('ffem',views.ffem,name='ffem'),
    path('exam',views.exam,name='exam'),
    path('start_exam/<str:subject>',views.start_exam,name='start_exam'),
    path('view_question/<str:subject>',views.view_question,name='view_question'),
    path('delete_test/<str:subject>',views.delete_test,name='delete_test'),
    path('submit_response',views.submit_response,name='submit_response'),
    
    path('', views.ffem,name='ffem')
]