from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm,Contact,Dashboardform
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Dashboard

def signup(request):
    if request.method == "POST":
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request,'account created successfully')
            fm.save()

    else:
        fm=SignUpForm()

    return render(request,'signup.html',{'form':fm})



def ulogin(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully !!')
                return HttpResponseRedirect('/dashboard/')
        else:
            fm = AuthenticationForm()
        return render(request, 'login.html', {'form':fm})
    else:
       return HttpResponseRedirect('/dashboard/')






def Logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == 'POST':
        fm = Contact(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Thanks for Contacting Us')
            return HttpResponseRedirect("<h1> Succussfull </h1>")

    else:
        fm = Contact()
    return render(request,'contact.html',{'form':fm})


def home(request):
    blogs = Dashboard.objects.all()
    return render(request, 'home.html', {'blog': blogs})



def dashboard(request):
    if request.method == "POST":
        fm = Dashboardform(request.POST)
        if fm.is_valid():
            messages.success(request, 'Updated')
            fm.save()
    else:
      fm = Dashboardform()
    return render(request, 'dashboard.html', {'form':fm})



def ulogout(request):
  logout(request)
  return HttpResponseRedirect('/login/')


def deleteb(request,id):
    fm=Dashboard.objects.get(pk=id)
    fm.delete()
    return HttpResponseRedirect('/home/')

def editb(request, id):
    fm = Dashboard.objects.get(pk=id)
    form = Dashboardform(instance=fm)
    if request.method == 'POST':
        form = Dashboardform(request.POST, instance=fm)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/home/')
    else:
        return render(request, 'edit.html', {'form': form})