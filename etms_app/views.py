#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

from django.shortcuts import render, redirect
from . models import Employee,Task
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib import auth
# Create your views here.

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def signup(request):
    if request.method == 'POST':
        name= request.POST['signup-name']
        email = request.POST['signup-email']
        pswd1 = request.POST['signup-password1']
        pswd2 = request.POST['signup-password2']
        
        
        if pswd1 == pswd2:
            if User.objects.filter(username=name).exists():
                messages.error(request,"Username allready exists")
                return redirect("/signup")  
            
            elif User.objects.filter(email=email).exists():
                 messages.error(request,"Email allready exists")
                 return redirect("/signup")  
            else:
                User.objects.create_user(first_name=name, username= name, email=email, password=pswd1)    
                
                messages.error(request,"Your account created successfully")
                return redirect("/login")  
        else:
            messages.error(request,"passwords do not match")
            return redirect("/signup")  
        
    return render(request, 'signup.html')


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def login(request):
             
    if request.method == 'POST':
      
        #DATA COLLECT FROM FORM
        uname = request.POST['uname']
        pswd = request.POST['signin-password']
        
        #AUTHENTICATE THE USER WHETHER IT EXIST OR NOT
        user = auth.authenticate(request, username=uname, password=pswd)
        
        #if user authencticate hai mtlb kutch na kutch user mila h.
        if user is not None:
            auth.login(request, user=user)
            if request.user.is_superuser:
                messages.info(request,"login successfully!")
                return redirect("/admin")
            else:
                messages.info(request,"login successfully!")
                return redirect("/dashboard")
                
        else:
            messages.error(request,"Invalid crendential and try again")
            return redirect("/login")
    else:
        return render(request, 'login.html')


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def logout(request):
    messages.success(request,"Logged out successfully!")
    auth.logout(request)
    return redirect('/login')



#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


@login_required(login_url='/login')
def dashboard(request):
    user = request.user
    #completed = Task.objects.filter(doc__is_null = False)
    #pending = Task.objects.filter(doc__is_null = True)
    
    employee = Employee.objects.get(user=user)#(fix user=variable user) or employee = user.employee
    pending_tasks = Task.objects.filter(employee = employee, doc__isnull = True)
    
    completed_tasks = Task.objects.filter(employee = employee, doc__isnull = False) #doc = deadline
    
        
    context = {
        'emp' : employee,
        'completed': completed_tasks,
        'pending': pending_tasks,     
             
    }
   
    print("You are an employee")      
    return render(request, 'emp_dashboard.html', context)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

@login_required(login_url='/login')
def mark_as_completed(request, id):
    task = Task.objects.get(id=id)
    task.doc = datetime.now()
    task.save()
    return redirect("/dashboard")


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

@login_required(login_url='/login')
def my_account(request):
    user = request.user
    emps = Employee.objects.get(user=user)                          #(fix user=variable user) or employee = user.employee
    completed_tasks = Task.objects.filter(employee=emps, doc__isnull = False).count() #doc = deadline
    context = {
        'emp' : emps,
        'completed': completed_tasks,
             
    }
    return render(request,'account.html',context)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


@login_required(login_url='/login')
def tasks(request):
    user = request.user
  
    #completed = Task.objects.filter(doc__is_null = False)
    #pending = Task.objects.filter(doc__is_null = True)
    
    emps = Employee.objects.get(user=user)                          #(fix user=variable user) or employee = user.employee
    pending_tasks = Task.objects.filter(employee=emps, doc__isnull = True).count()
    
    completed_tasks = Task.objects.filter(employee=emps, doc__isnull = False).count() #doc = deadline
    
        
    context = {
        'emp' : emps,
        'completed': completed_tasks,
        'pending': pending_tasks,     
             
    }
    return render(request,'emp_tasks.html',context)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


def update(request,pk):
    #FETCH THE OBJECTS THATS NEEDS TO BE EDITED
    emps = Employee.objects.get(id=pk)
    
    if request.method == 'POST':
        #VALUES FETCH FROM templates 
        name = request.POST['name'] 
        phone = request.POST['phone']
        address = request.POST['address']
        
        
        #VALUES OVERWRITE
        emps.name = name
        emps.phone = phone
        emps.address = address
        
        
        #SAVES THE OBJECT
        emps.save()
        messages.success(request,"You have updated successfully")
        
        #REDIRECT TO DASHBOARD
        return redirect("/dashboard")   
    context = {
    'emp' : emps,
    }
    return render(request,'update_profile.html', context)
    
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  
      
def emp_delete_task(request,pk):
    #FETCH THE BLOG
    task = Task.objects.get(id=pk)
    
    #DELETE THE BLOG
    task.delete()
    #REDIRECT TO DASHBIARD
    
    messages.success(request,"You have deleted successfully")
    
    return redirect("/dashboard")
    

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@