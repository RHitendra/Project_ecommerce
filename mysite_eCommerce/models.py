from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class ShippingAddress(models.Model):
    user_id = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    Addressline1 = models.CharField(max_length=300)
    Addressline2 = models.CharField(max_length=300)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=90)
    Zipcode = models.CharField(max_length=30)
    Country = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user_id)+" "+str(self.City)



class Customer(models.Model):
    user_id = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    mobile_no= models.CharField(max_length=10, blank=True)
    alter_mobile = models.CharField(max_length=10, blank=True)
    address = models.ManyToManyField(ShippingAddress)

    def __str__(self):
        return str(self.user_id)



class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True, blank=True)
    date_order = models.DateTimeField(auto_now_add=True)
    Completed = models.BooleanField(default=False,null=True,blank=True)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.Quantity for item in orderitems])
        return total

class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=20)
    product_category=models.CharField(max_length=220,default='')
    product_desc=models.CharField(max_length=500, default='')
    product_price=models.FloatField(default=0)
    product_dtae=models.DateField()
    product_image=models.ImageField(upload_to='mysite_eCommerce/images',default='')
    product_quantity = models.IntegerField(default=0)
    product_brand = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.product_name


class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    Quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.product_price * self.Quantity
        return total