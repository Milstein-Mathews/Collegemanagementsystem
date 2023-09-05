from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.home,name='home'),
    path('signin1',views.signin1,name='signin1'),
    path('signin2',views.signin2,name='signin2'),
    path('signup',views.signup,name='signup'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('add_course',views.add_course,name='add_course'),
    path('add_courseurl',views.add_courseurl,name='add_courseurl'),
    path('add_student',views.add_student,name='add_student'),
    path('add_studenturl',views.add_studenturl,name='add_studenturl'),
    path('show_student',views.show_student,name='show_student'),
    path('editstudent/<int:pk>',views.editstudent,name='editstudent'),
    path('editstudenturl/<int:pk>',views.editstudenturl,name='editstudenturl'),
    path('deletestudent/<int:pk>',views.deletestudent,name='deletestudent'),
    path('add_teacher',views.add_teacher,name='add_teacher'),
    path('show_teacher',views.show_teacher,name='show_teacher'),
    path('deleteteacher/<int:pk>',views.deleteteacher,name='deleteteacher'),
    path('teacher_home',views.teacher_home,name='teacher_home'),
    path('profile',views.profile,name='profile'),
    path('edit_teacher',views.edit_teacher,name='edit_teacher'),
    path('logout',views.logout,name='logout'),

]