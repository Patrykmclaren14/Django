from django.shortcuts import redirect, render , HttpResponse
from datetime import datetime
import calendar
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Task, Step

# Create your views here.

def home(request):
    current_date = datetime.now().date()
    day_of_week = calendar.day_name[current_date.weekday()]
    my_date = f"{day_of_week}, {current_date.day} {calendar.month_name[current_date.month]} {current_date.year}"
    
    

    if request.method == 'POST':
        name = request.POST['name']
        user = request.user
        Task.objects.create(name=name, user=user, date=current_date)
        return redirect('home')
    
    tasks = None 
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
    
    return render(request, 'home.html', {'date': my_date, 'tasks': tasks})



def update(request, task_id, step_id):
    if request.method == 'POST':
        if 'update_task' in request.POST:
            task = Task.objects.get(id=task_id)
            task.status = 'done'
            task.save()

        elif 'important_task' in request.POST:
            task = Task.objects.get(id=task_id)
            task.important = 'important'
            task.save()
            
        elif 'upload_date' in request.POST:
            task = Task.objects.get(id=task_id)
            task.date = request.POST['date']
            task.save()

        elif 'update_task_important' in request.POST:
            task = Task.objects.get(id=task_id)
            task.status = 'done'
            task.save()
            return redirect('important')
        
        elif 'file' in request.FILES:
            task = Task.objects.get(id=task_id)
            task.file = request.FILES['file']
            task.save()
            return redirect(f'/task/{task_id}')
        
        elif 'upload_note' in request.POST:
            task = Task.objects.get(id=task_id)
            task.note = request.POST['note']
            task.save()
            return redirect(f'/task/{task_id}')
        
        elif 'upload_step' in request.POST:
            step_name = request.POST['step']
            task = Task.objects.get(id=task_id)
            
            if task.steps.count() < 5:
                step = Step.objects.create(name=step_name)
                task.steps.add(step)
            
            return redirect(f'/task/{task_id}')
        
        elif 'upload_user' in request.POST:
            username = request.POST['user']
            task = Task.objects.get(id=task_id)
            user = User.objects.get(username=username)
                
            task.assigned_users.add(user)
                
            return redirect(f'/task/{task_id}')
        
        if 'step_delete' in request.POST:
            step_id = request.POST['step_delete']
            step = Step.objects.get(id=step_id)
            step.delete()
            return redirect(f'/task/{task_id}')

        
    return redirect('home')
        


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else: 
            messages.success(
            request, ("Invalid data"))
            return redirect('login-view')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login-view')

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.success(
            request, ("Password is not the same"))
            return render(request, 'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.success(
            request, ("User already exists"))
            return render(request, 'register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        return redirect('login')
        
    return render(request, 'register.html')


def task(request, task_id):
    current_date = datetime.now().date()  
    day_of_week = calendar.day_name[current_date.weekday()]  
    my_date = f"{day_of_week}, {current_date.day} {calendar.month_name[current_date.month]} {current_date.year}" 

    if request.method == 'POST':
        name = request.POST['name']
        user = request.user
        Task.objects.create(name=name, user=user, date=current_date)
        return redirect(f'/task/{task_id}')

    
    tasks = None 
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
    steps = Step.objects.all()
    task = Task.objects.get(id=task_id)
    return render(request, 'task.html', {'tasks': tasks, 'date':my_date, 'task': task, 'steps': steps})

def important(request):
    tasks = None 
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)

    return render(request, 'important.html', {'tasks': tasks})

def done(request):
    tasks = None 
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)

    return render(request, 'done.html', {'tasks': tasks})

def show(request):
    tasks = None 
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)

    return render(request, 'show.html', {'tasks': tasks})

def show_task(request, task_id):
    current_date = datetime.now().date()  
    day_of_week = calendar.day_name[current_date.weekday()]  
    my_date = f"{day_of_week}, {current_date.day} {calendar.month_name[current_date.month]} {current_date.year}" 

    task = Task.objects.get(id=task_id) 
    return render(request, 'show_task.html', {'date':my_date, 'task': task})

def search_view(request):
    if request.method == "POST":
        current_date = datetime.now().date()  
        day_of_week = calendar.day_name[current_date.weekday()]  
        my_date = f"{day_of_week}, {current_date.day} {calendar.month_name[current_date.month]} {current_date.year}" 

        searched = request.POST['searched']
        tasks = Task.objects.filter(name__contains=searched)
        return render(request, 'search.html', {'date':my_date, 'searched': searched, 'tasks': tasks})
    else:
        return render(request, 'search.html')
    
def groupe(request):
    current_date = datetime.now().date()
    day_of_week = calendar.day_name[current_date.weekday()]
    my_date = f"{day_of_week}, {current_date.day} {calendar.month_name[current_date.month]} {current_date.year}"
    tasks = Task.objects.filter(assigned_users=request.user)  # Filter tasks based on the requesting user being in assigned_users
    return render(request, 'groupe.html', {'date': my_date, 'tasks': tasks})





