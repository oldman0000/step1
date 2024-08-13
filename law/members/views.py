from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from .forms import ResisterUserForm




# Create your views here.


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('step1:index')
        else:
            messages.success(request, ("there was an Error"))
            return redirect('login_user')
    else:
        return render(request,"auth/login.html",{
            
        })





def logout_user(request):
    logout(request)
    messages.success(request, ("You were loged out"))
    return redirect('step1:index')


def register_user(request):
    
    
    if request.method == "POST":
        
        form = ResisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            
            password = form.cleaned_data['password1']
            username = form.cleaned_data['username']
            
            user = authenticate(password=password, username=username)
            login(request, user)   
            messages.success(request, ("Registration was successfull"))   
            return redirect('step1:list_venue')  
        
        
    else:
        form = ResisterUserForm()
            
        
        
    return render(request, "auth/register_user.html",{
        "form": form,
    })
    

 