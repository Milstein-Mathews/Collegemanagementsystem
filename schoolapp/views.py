from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.models import User, auth
from django.contrib import messages
from schoolapp.models import Course
from schoolapp.models import Student,Teacher
from django.contrib.auth.decorators import login_required
import os

# Create your views here.
def home(request):
    return render(request,'home.html')
def signin1(request):
    return render(request,'login.html')
def signin2(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        admin = auth.authenticate(username=username, password=password)
        
        if admin is not None:
            if admin.is_staff:
                login(request,admin)
                return redirect('admin_home')
            else:
                login(request,admin)
            # request.session['uid'] = user.id
                auth.login(request, admin)
                messages.info(request, f'welcome {username}')
                return redirect('teacher_home')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('signin1')
    else:
        return redirect('signin1')
def signup(request):
    courses=Course.objects.all()
    return render(request,'signup.html',{'course':courses})
@login_required(login_url='signin1')
def admin_home(request):
    return render(request,'admin_home.html')
@login_required(login_url='signin1')
def add_course(request):
    return render(request,'add_course.html')
@login_required(login_url='signin1')
def add_courseurl(request):
    if request.method == 'POST':
        course_name=request.POST['name']
        course_fee=request.POST['fee']
        course=Course(course_name=course_name,fee=course_fee)
        course.save()
        return redirect('add_course')
    return render(request,'add_course.html')
@login_required(login_url='signin1')
def add_student(request):
    courses=Course.objects.all()
    return render(request,'add_student.html',{'course':courses})
@login_required(login_url='signin1')
def add_studenturl(request):
    if request.method == 'POST':
        student_name=request.POST['name']
        student_address=request.POST['address']
        age=request.POST['age']

        date=request.POST['date']
        select=request.POST['select']
        course=Course.objects.get(id=select)
        student=Student(student_name=student_name,student_address=student_address,student_age=age,joining_date=date,course=course)
        student.save()
        return redirect('add_student')
    return render(request,'add_student.html')
@login_required(login_url='signin1')
def show_student(request):
    student=Student.objects.all()
    return render(request,'show_student.html',{'students':student})
@login_required(login_url='signin1')
def editstudent(request,pk):
    student=Student.objects.get(id=pk)
    course=Course.objects.all()
    return render(request, 'edit_student.html', {'stud': student, 'course': course})
@login_required(login_url='signin1')
def editstudenturl(request,pk):
    if request.method == 'POST':
        student=Student.objects.get(id=pk)
        student.student_name=request.POST['name']
        student.student_address=request.POST['address']
        student.student_age=request.POST['age']

        student.joining_date=request.POST['date']
        select=request.POST['course']
        course1=Course.objects.get(id=select)
        student.course=course1
        student.save()
        return redirect('show_student')
    return render(request,'edit_student.html')
@login_required(login_url='signin1')
def deletestudent(request,pk):
    stud=Student.objects.get(id=pk)
    stud.delete()
    return redirect('show_student')


def add_teacher(request):
    if request.method=='POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        username=request.POST['username']
        password=request.POST['password']
        cfmpassword=request.POST['cfmpassword']
        address=request.POST['address']
        age=request.POST['age']
        email=request.POST['mail']
        contact=request.POST['contact']
        image = request.FILES.get('file')
        select=request.POST.get('select')
        course=Course.objects.get(id=select)


        if password==cfmpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'This username already exists')
                return redirect('signup')
            else:
                user=User.objects.create_user(first_name=firstname,last_name=lastname,username=username,password=password,email=email)
                user.save()
                tech=Teacher(address=address,age=age,contact_number=contact,image=image,course=course,user=user)
                tech.save()
        else:
            messages.info(request, "Password doesn't match")
            return redirect('signup')   
        return redirect('signin1')
    else:
        return render(request,'login.html')
    
@login_required(login_url='signin1')
def show_teacher(request):
    teacher=Teacher.objects.all()
    return render(request,'show_teacher.html',{'teacher':teacher})
@login_required(login_url='signin1')
def deleteteacher(request,pk):
    t1=Teacher.objects.get(user=pk)
    t1.delete()
    t=User.objects.get(id=pk)
    t.delete()
    return redirect('show_teacher')

@login_required(login_url='signin1')
def teacher_home(request):
    return render(request,'teacher_home.html')

@login_required(login_url='signin1')
def profile(request):
    user1=request.user.id
    teachers=Teacher.objects.get(user=user1)
    return render(request,'profile.html',{'teacher': teachers})

@login_required(login_url='signin1')
def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required(login_url='signin1')
def edit_teacher(request):
    if request.user.is_authenticated:
        current_user=request.user.id
        user1=Teacher.objects.get(user=current_user)
        user2=User.objects.get(id=current_user)
        cour=Course.objects.all()
        if request.method=='POST':
                if len(request.FILES)!=0:
                    if len(user1.image)>0:
                        os.remove(user1.image.path)
                    user1.image=request.FILES.get('file')
                user2.first_name=request.POST['firstname']
                user2.last_name=request.POST['lastname']
                user2.username=request.POST['username']
                user1.address=request.POST['address']
                user1.age=request.POST['age']
                user2.email=request.POST['mail']
                user1.contact_number=request.POST['contact']
                select=request.POST['select']
                course1=Course.objects.get(id=select)
                user1.course=course1
                user1.save()
                user2.save()
                return redirect('profile')
        return render(request,'edit_teacher.html',{'teacher': user1,'course':cour})