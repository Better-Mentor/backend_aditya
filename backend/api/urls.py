
from django.urls import path
from . import views

urlpatterns = [
    path('student/dashboard', views.student_dashboard, name='student_dashboard'),
    path('student/takemcq', views.take_mcq, name='take_mcq'),
    path('student/analyzemcq', views.analyze_mcq, name='analyze_mcq'),
    path('teacher/allclasses/<int:teacherid>', views.all_classes, name='all_classes'),
    path('teacher/class/<int:classID>', views.class_details, name='class_details'),
    path('teacher/class/stud/<int:studentID>', views.student_details, name='student_details'),
    path('teacher/uploadMCQ', views.upload_mcq, name='upload_mcq'),
]
