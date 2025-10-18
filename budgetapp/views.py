from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CreateUserForm
from django.contrib import messages
# from django.contrib.auth.decorators import login_required

# def main(request):
#     if request.method == "POST":
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             login(request, form.get_user())
#             return redirect("dashboard")
#     else:
#         form = AuthenticationForm()
#     return render(request, "main.html" , {"form" : form })

def loginpage(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("dashboard")
    else:
        form = AuthenticationForm()

    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, "loginpage.html" , {"form" : form })

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("dashboard")
            #user = form.cleaned_data.get('username')
            #messages.success(request, " Account was created for " + user)
        else:
            print(form.errors)
            return redirect("register")
        
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    context = {"form" : form }
    return render(request, "register.html" , context)

# @login_required()
def dashboard(request):
    return render(request,"dashboard.html")

def logout_view(request):
     if request.method == "POST":
          logout(request)
          return redirect("loginpage")