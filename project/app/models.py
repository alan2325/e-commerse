from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

class Register(models.Model):
    Email = models.EmailField(unique=True)
    name = models.TextField()
    phonenumber = models.IntegerField()
    password = models.TextField()
    location= models.TextField()

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.TextField()
    discription = models.TextField()
    price = models.IntegerField()
    category = models.TextField()
    quantity = models.IntegerField()
    offerprice = models.IntegerField()
    image = models.FileField()

    def __str__(self):
        return self.name
    
class cart(models.Model):
    user = models.ForeignKey(Register,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.user.name +' '+self.product.name
    
    def total_price(self):
        return self.quantity * self.product.price
    

 
class buy(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Register,on_delete=models.CASCADE)
    date_of_buying = models.TextField()
    # payment_status = models.BooleanField(default=False)
    # order_status = models.IntegerField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    # del_boy=models.BooleanField(default=False)
    DELIVERY_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Shipped", "Shipped"),
        ("In Transit", "In Transit"),
        ("Delivered", "Delivered"),
    ]
    delivery_status = models.CharField(
        max_length=20, choices=DELIVERY_STATUS_CHOICES, default="Pending"
    )

    # Optional: define a string representation for clarity in admin
    def __str__(self):
        return f"{self.product.name} - {self.delivery_status}"
    
       
# class buy(models.Model):
#     user = models.ForeignKey(Register,on_delete=models.CASCADE)
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     date_of_buying = models.TextField()
#     payment_status = models.BooleanField(default=False)
#     # order_status = models.IntegerField()
#     quantity = models.IntegerField()
#     price = models.IntegerField()


#     def __str__(self):
#         return self.user.name
    



# class Delreg(models.Model):
#     Email = models.EmailField(unique=True)
#     name = models.TextField()
#     phonenumber = models.IntegerField()
#     password = models.IntegerField()
#     delroot = models.TextField()

#     def __str__(self):
#         return self.name

class Delreg(models.Model):
    rout = models.TextField()
    email =  models.EmailField(unique=True)
    password = models.TextField()
    name = models.TextField()
    phonenumber = models.IntegerField()
    def _str_(self):
        return self.name

class delpro(models.Model):
    delivery=models.ForeignKey(Delreg,on_delete=models.CASCADE)
    buy=models.ForeignKey(buy,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    date=models.TextField(null=True)    
