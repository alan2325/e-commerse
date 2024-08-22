from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

class Register(models.Model):
    Email = models.EmailField(unique=True)
    name = models.TextField()
    phonenumber = models.IntegerField()
    password = models.IntegerField()
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
    
class buy(models.Model):
    user = models.ForeignKey(Register,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date_of_buying = models.TextField()
    payment_status = models.BooleanField(default=False)
    # order_status = models.IntegerField()
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.name

