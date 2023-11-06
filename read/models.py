from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
import datetime



class Registration(models.Model):
    First_name = models.CharField(max_length=200)
    Last_name = models.CharField(max_length=200)
    Email = models.EmailField(max_length=200)
    Password = models.CharField(max_length=200)
    Registration_date = models.DateField()
    About_website = models.TextField()
    User_role = models.CharField(max_length=200)
    user = models.OneToOneField(User,on_delete = models.CASCADE, null = True)
    Image = models.ImageField(upload_to='media')


    def __str__(self):
        return self.First_name

class Joining(models.Model):
    User_name = models.CharField(max_length=200)
    User_email = models.EmailField()
    Staff_name = models.CharField(max_length=200)
    Staff_email = models.EmailField()
    Joining_date = models.DateField(auto_now_add=True)
    notify = models.CharField(max_length=200, null = True)
    join_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True)

class Requests(models.Model):
    Name = models.CharField(max_length=200)
    Email = models.EmailField()
    User_category = models.CharField(max_length=200)
    Old_password = models.CharField(max_length=200)
    New_password = models.CharField(max_length=200)
    Req_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True)

class Category(models.Model):
    name = models.CharField(max_length=200)
    
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='media/', blank=True)

    @staticmethod
    def get_products_id(ids):
        return Product.objects.filter(name__in = ids)

    def __str__(self):
        return self.name
    @staticmethod
    def get_all_products():
        return Product.objects.all()
    @staticmethod
    def get_all_products_by_id(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_products()

class Order(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    user = models.ForeignKey(Registration , on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=200, default='' , blank=False)
    phone = models.CharField(max_length=50 , default='' , blank=False)
    pincode = models.CharField(max_length=50 , default='' , blank=False)
    date = models.DateField(max_length=50 , default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    
    def placeorder(self):
        self.save()
        
    @staticmethod
    def get_orders_by_user(user_id):
        return Order\
            .objects\
                .filter(user = user_id)\
                    .order_by('-date')
                
