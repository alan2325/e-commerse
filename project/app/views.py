from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages

# Create your views here.

def login(req):
    if req.method=='POST':
        email=req.POST['Email']
        password=req.POST['password']
        try:
            data=Register.objects.get(Email=email,password=password)
            return redirect(userhome)
        except:

            messages.warning(req, "INVALID INPUT !")
    return render(req,'login.html')

def register(req):

    if req.method=='POST':
        name1=req.POST['name']
        email2=req.POST['email']
        phonenumber3=req.POST['phonenumber']
        location4=req.POST['location']
        password5=req.POST['password']
        try:
            data=Register.objects.create(name=name1,Email=email2,phonenumber=phonenumber3,location=location4,password=password5)
            data.save()
            return redirect(login)
        except:
            messages.warning(req, "Email Already Exits , Try Another Email.")
    return render(req,'register.html')

def userhome(req):
    return render(req,'userhome.html')

def adminhome(req):
    return render(req,'adminhome.html')