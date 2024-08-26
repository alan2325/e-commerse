from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User,auth
import datetime
# Create your views here.

def get_usr(req):
    data=Register.objects.get(Email=req.session['user'])
    return data




def login(req):
    if 'user' in req.session:
        return redirect(user_home)
    if 'shop' in req.session:
        return redirect(adminhome)
    # if 'delivery' in req.session:
    #     return redirect(delivery)
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
        


            messages.warning(req, "INVALID INPUT !")
    return render(req,'login.html')


def logout(req):
    if 'user' in req.session:
        del req.session['user']
    if 'shop' in req.session:
        del req.session['shop']
    # if 'delivery' in req.session:
    #     del req.session['delivery']
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



###profile
def profile(req):
    if 'user' in req.session:
        # data=Register.objects.get(Email=req.session['user'])
        return render(req,'user/profile.html',{'data':get_usr(req)})
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
        return render(req,'user/upload.html',{'data':data})

    else:
       return redirect(login)
    
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
def deletes(req,id):
    data=cart.objects.get(pk=id)
    data.delete()
    return redirect(user_view_cart)


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


  

    # return render(req, 'buy.html', {'cart_items': cart_items, 'total_price': total_price})

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

def order_details(req):
    if 'user' in req.session:
        data=buy.objects.filter(user=get_usr(req))
        return render(req,'user/orderdetails.html',{'data':data})
    else:
        return redirect(login)
def user_home(req):
    if 'user' in req.session:
        return render(req,'user/user_home.html')
    else:
        return redirect(login)


      
def usr_pro_display(req,id):
    if 'user' in req.session:
        data=Product.objects.get(pk=id)
        return render(req,'user/usr_pro_display.html',{'data':data})
    else:
        return redirect(login)
   

#### shop



def adminhome(req):
    if 'shop' in req.session:
        return render(req,'shop/adminhome.html')
    else:
        return redirect(login)     
def viewuser(req):
    if 'shop' in req.session:
        data=Register.objects.all
        return render(req,'shop/viewuser.html',{'data':data})
    else:
        return redirect(login) 

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

def viewpro(req):
    if 'shop' in req.session:
        data=Product.objects.all()
        return render(req,'shop/viewpro.html',{'data':data})
    else:
        return redirect(login) 

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
    




# ###delivery
def delivery_home(req):
    return render(req,'delivery/delivery_home.html')

# def delivery_reg(req):
#       if req.method=='POST':
#         name1=req.POST['name']
#         email2=req.POST['email']
#         phonenumber3=req.POST['phonenumber']
#         delroot=req.POST['root']
#         password5=req.POST['password']
#         try:
#             data=Delreg.objects.create(name=name1,Email=email2,phonenumber=phonenumber3,delroot=delroot,password=password5)
#             data.save()
#             return redirect(login)
#         except:
#             messages.warning(req, "Email Already Exits , Try Another Email.")
    
#         return render(req,'delivery/delivery_reg.html')
      
def delivery(req):
    data=buy.objects.filter(user=get_usr(req))
    return render(req,'delivery/new_delivery.html',{'data':data })
