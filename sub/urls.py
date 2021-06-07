from django.urls import path
from . import views

urlpatterns = [
    path('setexam',views.setexam,name='setexam'),
    path('faculty',views.faculty,name='faculty'),
    path('ffem',views.ffem,name='ffem'),
    path('exams',views.exams,name='exams'),
    path('start_exam/<str:subject>',views.start_exam,name='start_exam'),
    path('view_question/<str:subject>',views.view_question,name='view_question'),
    path('delete_test/<str:subject>',views.delete_test,name='delete_test'),
    # path('index/<str:year>',views.index,name='index'),
    path('report_details/<str:subject>',views.report_details,name='report_details'),
    path('view_report',views.view_report,name='view_report'),
    path('', views.ffem,name='ffem')
]