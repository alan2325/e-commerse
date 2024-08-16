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

def profile(req):
    return render(req,'profile.html')

def upload(req):

    # user={}
    # pos=0
    # for i in register:
    #     if i['id']==user:
    #         std1=i
    #         pos=register.index(i)

    # if req.method=='POST':
    #     Email=req.POST['Email']
    #     name=req.POST['name']
    #     phonenumber=req.POST['phonenumber']
    #     password=req.POST['password']
    #     location=req.POST['location']
    #     register[pos]={'Email':Email,'name':name,'phonenumber':phonenumber,'password':password,'location':location}
    #     return redirect(profile)

    # else:
    #    return render(req,'upload.html',{'data':std1})
      return render(req,'upload.html')

     
