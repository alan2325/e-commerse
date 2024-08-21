from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User,auth
# Create your views here.

def get_usr(req):
    data=Register.objects.get(Email=req.session['user'])
    return data




def login(req):
    if 'user' in req.session:
        return redirect(userhome)
    if 'shop' in req.session:
        return redirect(adminhome)
    if req.method=='POST':
        email=req.POST['Email']
        password=req.POST['password']
        try:
            data=Register.objects.get(Email=email,password=password)
            req.session['user']=data.Email
            return redirect(userhome)
        except:
            shop=auth.authenticate(username=email,password=password)
            if shop is not None:
                auth.login(req,shop)
                req.session['shop']=email

                return redirect(adminhome)


            messages.warning(req, "INVALID INPUT !")
    return render(req,'login.html')


def logout(req):
    if 'user' in req.session:
        # req.session.flush()
        del req.session['user']
    if 'shop' in req.session:
        del req.session['shop']
    return redirect(login)
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
    if 'user' in req.session:
        return render(req,'userhome.html')
    else:
        return redirect(login)


###profile
def profile(req):
    if 'user' in req.session:
        # data=Register.objects.get(Email=req.session['user'])
        return render(req,'profile.html',{'data':get_usr(req)})
    else:
        return redirect(login)
    
###profile update
def upload(req):
    if 'user' in req.session:
        data=Register.objects.get(Email=req.session['user'])
        if req.method=='POST':
            name=req.POST['name']
            phonenumber=req.POST['phonenumber']
            location=req.POST['location']
            Register.objects.filter(Email=req.session['user']).update(name=name,phonenumber=phonenumber,location=location)
            return redirect(profile)
        return render(req,'upload.html',{'data':data})

    else:
       return redirect(login)
    
def viewproduct(req):
    data=Product.objects.all()
    return render(req,'viewproduct.html',{'data':data})

def user_cart(req,id):
    if 'user' in req.session:
        product=Product.objects.get(pk=id)
        user=get_usr(req)
        qty=1
        try:
            dtls=cart.objects.get(product=product,user=user)
            dtls.quantity+=1
            dtls.save()
        except:
            data=cart.objects.create(product=product,user=user,quantity=qty)
            data.save()
        return redirect(user_view_cart)
    else:
        return redirect(login)
    
def user_view_cart(req):
    if 'user' in req.session:
        data=cart.objects.filter(user=get_usr(req))
        return render(req,'cart.html',{'data':data})
def deletes(req,id):
    data=cart.objects.get(pk=id)
    data.delete()
    return redirect(user_view_cart)

def singlepro(req):
    return render(req,'singlepro.html')

def buys(req):
    cart_items = cart.objects.filter(user=req.user)
    total_price = sum(item.total_price() for item in cart_items)

    if req.method == 'POST':
        # Process the order here
        # For example, save the order to the database, charge the user, etc.
        # After processing, you might want to clear the cart:
        cart_items.delete()
        return redirect('order_success')  # Redirect to an order success page

    return render(req, 'buy.html', {'cart_items': cart_items, 'total_price': total_price})

def qty_incri(req,id):
    data=cart.objects.get(pk=id)
    data.quantity+=1
    data.save()
    return redirect(user_view_cart)


def qty_decri(req,id):
    data=cart.objects.get(pk=id)
    if data.quantity>1:
        data.quantity-=1
        data.save()
    return redirect(user_view_cart)


#### shop



def adminhome(req):
    if 'shop' in req.session:
        return render(req,'adminhome.html')
    else:
        return redirect(login)     
def viewuser(req):
    return render(req,'viewuser.html')


def addpro(req):
    if req.method=='POST':
            name=req.POST['name']
            discription =req.POST['discription']
            price =req.POST['price']
            category =req.POST['category']
            quantity =req.POST['quantity']
            offerprice = req.POST['offerprice']
            image = req.FILES['image']
            data=Product.objects.create(name=name,discription=discription,price=price,category=category,quantity=quantity,offerprice=offerprice,image=image)
            data.save()
            return redirect(viewpro)
    return render(req,'addpro.html')


def viewpro(req):
    data=Product.objects.all()
    return render(req,'viewpro.html',{'data':data})


def bookinghistory(req):
    return render(req,'bookinghistory.html')


      
def prodetails(req,id):
    
        data=Product.objects.get(pk=id)
        return render(req,'prodetails.html',{'data':data})
    

def proupdate(req,id):
    data=Product.objects.get(pk=id)
    if req.method=='POST':
        name=req.POST['name']
        price=req.POST['price']
        offerprice=req.POST['offerprice']
        quantity=req.POST['quantity']
        Product.objects.filter(pk=id).update(name=name,price=price,offerprice=offerprice,quantity=quantity)
        return redirect(viewpro)
    return render(req,'proupdate.html',{'data':data})

def delete(req,id):
    data=Product.objects.get(pk=id)
    data.delete()
    return redirect(viewpro)
