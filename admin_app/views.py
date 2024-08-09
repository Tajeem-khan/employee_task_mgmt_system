#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

from django.shortcuts import render,redirect
from etms_app.models import Employee,Task
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime


# Create your views here.

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def dashboard(request):

    #completed = Task.objects.filter(doc__is_null = False)
    #pending = Task.objects.filter(doc__is_null = True)
    
    emps = Employee.objects.all().count()                             #(fix user=variable user) or employee = user.employee
    pending_tasks = Task.objects.filter(doc__isnull = True).count()
    
    completed_tasks = Task.objects.filter(doc__isnull = False).count() #doc = deadline
    
        
    context = {
        'emp' : emps,
        'completed': completed_tasks,
        'pending': pending_tasks,     
             
    }
   
    print("You are an employee")      
    return render(request ,'admin_dash.html',context)
    

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


def employees(request):
    employees = Employee.objects.all()
    return render(request, 'employees.html',{'employees':employees})


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


def tasks(request):
    
    pending_tasks = Task.objects.filter( doc__isnull = True)
    
    completed_tasks = Task.objects.filter( doc__isnull = False) #doc = deadline
    
        
    context = {
        'completed': completed_tasks,
        'pending': pending_tasks,     
             
    }
    print("You are an employee")      
    return render(request, 'tasks.html',context)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


def admin_add_task(request):
    emps = Employee.objects.all()
    if request.method == 'POST':
       #VALUE FETCHING
        title = request.POST['title'] 
        description = request.POST['description']
        deadline = request.POST['deadline'] 
        attachments = request.FILES['attachments']
        emps = request.POST['employees']
        employees = Employee.objects.get(name=emps)
    
       
      #CREATE A task OBJECT
        new_task = Task(title=title, description=description,  deadline=deadline, attachments=attachments, employee=employees)
        
        #SAVE THE OBJECT
        new_task.save() 
        messages.success(request,"Task assign successfully!")
        return redirect("/admin")
    return render(request, 'add-task.html',{'emp':emps})

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


