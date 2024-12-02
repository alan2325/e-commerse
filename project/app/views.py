from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User,auth
import datetime
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

### get email of user
def get_usr(req):
    data=Register.objects.get(Email=req.session['user'])
    return data



#### all login
def login(req):
    if 'user' in req.session:
        return redirect(user_home)
    if 'shop' in req.session:
        return redirect(adminhome)
    if 'delivery' in req.session:
        return redirect(delivery)
    if req.method=='POST':
        email=req.POST['Email']
        password=req.POST['password']
        try:
            data=Register.objects.get(Email=email,password=password)
            req.session['user']=data.Email
            return redirect(user_home)
        except:
            shop=auth.authenticate(username=email,password=password)
            if shop is not None:
                auth.login(req,shop)
                req.session['shop']=email

                return redirect(adminhome)
            else:
                data=delivery.objects.get(email=email,password=password)
                req.session['deliveryss']=data.email
                return redirect(delivery)

                messages.warning(req, "INVALID INPUT !")
    return render(req,'login.html')

### delete all session
def logout(req):
    if 'user' in req.session:
        del req.session['user']
    if 'shop' in req.session:
        del req.session['shop']
    if 'delivery' in req.session:
        del req.session['delivery']
    return redirect(login)

#### user registration
def register(req):
    if req.method=='POST':
        name1=req.POST['name']
        email2=req.POST['email']
        phonenumber3=req.POST['phonenumber']
        location4=req.POST['location']
        password5=req.POST['password']
        subject = 'Registration details '
        message = 'ur account uname {}  and password {}'.format(name1,password5)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email2]
        send_mail(subject, message, from_email, recipient_list,fail_silently=False)  
        try:
            data=Register.objects.create(name=name1,Email=email2,phonenumber=phonenumber3,location=location4,password=password5)
            data.save()
            return redirect(login)
        except:
            messages.warning(req, "Email Already Exits , Try Another Email.")
    return render(req,'register.html')

### user profile
def profile(req):
    if 'user' in req.session:
        # data=Register.objects.get(Email=req.session['user'])
        return render(req,'user/profile.html',{'data':get_usr(req)})
    else:
        return redirect(login)
    
### user profile update
def upload(req):
    if 'user' in req.session:
        data=Register.objects.get(Email=req.session['user'])
        if req.method=='POST':
            name=req.POST['name']
            phonenumber=req.POST['phonenumber']
            location=req.POST['location']
            Register.objects.filter(Email=req.session['user']).update(name=name,phonenumber=phonenumber,location=location)
            return redirect(profile)
        return render(req,'user/upload.html',{'data':data})
    else:
       return redirect(login)
    
### view all product
def viewproduct(req):
    if 'user' in req.session:
        data=Product.objects.all()
        return render(req,'user/viewproduct.html',{'data':data})
    else:
        return redirect(login)
    
### add product to cart
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

### view cart    
def user_view_cart(req):
    if 'user' in req.session:
        data=cart.objects.filter(user=get_usr(req))
        return render(req,'user/cart.html',{'data':data})
    else:
        return redirect(login)
    
### delete product from cart
def deletes(req,id):
    data=cart.objects.get(pk=id)
    data.delete()
    return redirect(user_view_cart)

### user buy productr
def buys(req,id):
    if 'user' in req.session:
        cart_product=cart.objects.get(pk=id)
        user=get_usr(req)
        quantity=cart_product.quantity
        date=datetime.datetime.now().strftime("%x")
        price=cart_product.product.price*quantity
        order=buy.objects.create(product=cart_product.product,user=user,quantity=quantity,date_of_buying=date,price=price)
        order.save()
        return redirect(user_view_cart)
    else:
        return redirect(login)

#### increase quantity in cart
def qty_incri(req,id):
    data=cart.objects.get(pk=id)
    data.quantity+=1
    data.save()
    return redirect(user_view_cart)

#### dectease quantity in cart
def qty_decri(req,id):
    data=cart.objects.get(pk=id)
    if data.quantity>1:
        data.quantity-=1
        data.save()
    return redirect(user_view_cart)

### user view all orders
def order_details(req):
    if 'user' in req.session:
        data=buy.objects.filter(user=get_usr(req))
        return render(req,'user/orderdetails.html',{'data':data})
    else:
        return redirect(login)
def user_home(req):
    if 'user' in req.session:
        data=Product.objects.all()
        return render(req,'user/user_home.html',{'data':data})
    else:
        return redirect(login)

### user product display     
def usr_pro_display(req,id):
    if 'user' in req.session:
        data=Product.objects.get(pk=id)
        return render(req,'user/usr_pro_display.html',{'data':data})
    else:
        return redirect(login)
   




###### shop/admin ######

### admin home
def adminhome(req):
    if 'shop' in req.session:
        return render(req,'shop/adminhome.html')
    else:
        return redirect(login)     
### admin view all users
def viewuser(req):
    if 'shop' in req.session:
        data=Register.objects.all
        return render(req,'shop/viewuser.html',{'data':data})
    else:
        return redirect(login) 

### admin add product
def addpro(req):
    if 'shop' in req.session:
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
        return render(req,'shop/addpro.html')
    else:
        return redirect(login) 

#### admin view product
def viewpro(req):
    if 'shop' in req.session:
        data=Product.objects.all()
        return render(req,'shop/viewpro.html',{'data':data})
    else:
        return redirect(login) 

#### view all booking history of all user
def bookinghistory(req):
    if 'shop' in req.session:
        data=buy.objects.all()
        return render(req,'shop/booking_history.html',{'data':data})
    else:
        return redirect(login) 

      
def prodetails(req,id):
    if 'shop' in req.session:
        data=Product.objects.get(pk=id)
        return render(req,'shop/prodetails.html',{'data':data})
    else:
        return redirect(login) 

def proupdate(req,id):
    if 'shop' in req.session:
        data=Product.objects.get(pk=id)
        if req.method=='POST':
            name=req.POST['name']
            price=req.POST['price']
            offerprice=req.POST['offerprice']
            quantity=req.POST['quantity']
            Product.objects.filter(pk=id).update(name=name,price=price,offerprice=offerprice,quantity=quantity)
            return redirect(viewpro)
        return render(req,'shop/proupdate.html',{'data':data})
    else:
        return redirect(login) 

def delete(req,id):
        data=Product.objects.get(pk=id)
        data.delete()
        return redirect(viewpro)
    




#########  delivery  ########

### delivery registration
def delregister(req):
    if req.method=='POST':
        name1=req.POST['name']
        email2=req.POST['email']
        phonenumber3=req.POST['phonenumber']
        location4=req.POST['rout']
        password5=req.POST['password']
        try:
            data=Delreg.objects.create(name=name1,email=email2,phonenumber=phonenumber3,rout=location4,password=password5)
            data.save()
            return redirect(login)
        except:
            messages.warning(req, "Email Already Exits , Try Another Email.")
    return render(req,'delivery/delregister.html')

def delivery_home(req):
    return render(req,'delivery/delivery_home.html')

      
def delivery(req):
    # data=buy.objects.filter(user=get_usr(req))
    return render(req,'delivery/new_delivery.html')

def deliverys(req):
    # data=buy.objects.filter(deliveryss=get_usr(req))
    # data1=Product.objects.filter(user=get_usr(req))
    return render(req,'delivery/delivery.html')

def assigndel(req,id):
    if req.method=='POST':
        data1=buy.objects.get(pk=id)
        data1.del_boy=True
        data1.save()
        data=req.POST['delselect'] 
        data2=Delreg.objects.get(pk=id)
        delivry=delpro.objects.create(delivery=data2,buy=data1) 
        delivry.save()

        return redirect(bookinghistry)
    
def bookinghistry(req):
    data=buy.objects.all()
    data1=Delreg.objects.all()
    return render(req,'delivery/bookinghistry.html',{'data':data,'data1':data1})