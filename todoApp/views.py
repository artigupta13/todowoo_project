from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm #form library
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def userprofile(request):
    # = User.get_short_name(request.user)
    profile=User.objects.get(username=request.user)
    username=profile.first_name
    return render(request,'todoApp/userprofile.html',{'profile':profile,'username':username})

def password_reset(request):
     if request.method=='GET':
         return render(request,'todoApp/password_reset_form.html')
     else:
         try:
             u = User.objects.get(username=request.POST['username'])
         except:
            return render(request,'todoApp/password_reset_form.html',{'error':'User does not exist'})

         if u is not None:
            if request.POST['password1']==request.POST['password2']:
                u.set_password(request.POST['password1'])
                u.save()
                return render(request,'todoApp/password_reset_form.html',{'success':'Password changed successfully'})
            else:
                return render(request,'todoApp/password_reset_form.html',{'error':'Password did not match'})
         else:
            return render(request,'todoApp/password_reset_form.html',{'error':'User does not exist'})



def home(request):
    return render(request,'todoApp/home.html')

# Create your views here.
def signupuser(request):
    if request.method=='GET':
        return render(request,'todoApp/signupuser.html',{'form':UserCreationForm()})
    else:
    #create new users
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'],password=request.POST['password1'],first_name=request.POST['first_name'],last_name=request.POST['last_name'])
                user.save()
                login(request,user)
                return redirect('currenttodos')

            except IntegrityError:
                return render(request,'todoApp/signupuser.html',{'form':UserCreationForm(),'error':'That username has already been taken. Please choose a new username'})


        else:
            return render(request,'todoApp/signupuser.html',{'form':UserCreationForm(),'error':'Password did not match'})

        #tell the user password didnt match
@login_required
def currenttodos(request):
    todos=Todo.objects.filter(user=request.user,datecompleted__isnull=True)
    #todos=Todo.objects.all()
    username = User.get_short_name(request.user)
    return render(request,'todoApp/currenttodos.html',{'todos':todos,'username':username})

def loginuser(request):
    if request.method=='GET':
        return render(request,'todoApp/loginuser.html',{'form':AuthenticationForm()})
    else:
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'todoApp/loginuser.html',{'form':AuthenticationForm(),'error':'Username or password did not match','forgotpassword':'Forgot Password?'})
        else:
            login(request,user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    username = User.get_short_name(request.user)

    if request.method=='GET':
            return render(request,'todoApp/createtodo.html',{'form':(TodoForm()),'username':username})
    else:
        try:
            form=TodoForm(request.POST)
            newtodo=form.save(commit=False)
            newtodo.user=request.user # to save particular user data
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return  render(request,'todo/createtodo.html',{'form':TodoForm(),'error':'Bad Data','username':first})
@login_required
def viewtodo(request,todo_pk):
    #todos=Todo.objects.all()
    username = User.get_short_name(request.user)
    todo=get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method=='GET':
        form=TodoForm(instance=todo)
        return render(request,'todoApp/viewtodo.html',{'todo':todo,'form':form,'username':username})
    else:
        try:
            form=TodoForm(request.POST,instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request,'todoApp/viewtodo.html',{'todo':todo,'form':form,'error':'Bad info','username':first})

@login_required
def completetodo(request,todo_pk):
    todo=get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method=='POST':
        todo.datecompleted=timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request,todo_pk):
    todo=get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method=='POST':
        todo.delete()
        return redirect('currenttodos')
@login_required
def completedtodos(request):
    username = User.get_short_name(request.user)
    todos=Todo.objects.filter(user=request.user,datecompleted__isnull=False).order_by('-datecompleted')
    #todos=Todo.objects.all()
    return render(request,'todoApp/completedtodos.html',{'todos':todos,'username':username})
