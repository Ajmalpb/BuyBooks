import datetime
import requests
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User, auth
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from .models import Product, Category , Registration , Order , Joining
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.http import require_GET, require_POST
from .forms import OrderStatusForm


def home(request):
    products = Product.get_all_products()
    return render(request, 'home.html', {'prds': products})


def about(request):
    return render(request, 'about.html')

def blog(request):
    return render(request, 'blog.html')

def contact(request):
    return render(request, 'contact.html')


def sgrid(request):
    if request.method == 'POST':        
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity -1
                else:
                    cart[product] = quantity +1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print(request.session['cart'])
        return redirect('sgrid')
    else:
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = Product.get_all_products()
        categories = Category.get_all_categories()
        if 'cart' not in request.session:
            request.session['cart'] = {}
        return render(request, 'shop-grid.html',{'prds': products, 'category': categories , 'cart': request.session['cart']})


def register(request):
    return render(request, 'login.html')


def register_staff(request):
    if request.method == 'POST':
        x = datetime.datetime.now()
        y = x.strftime("%Y-%m-%d")
        typ = request.POST.get('staff')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mgn = Registration.objects.all()
        for w in mgn:
            if w.Email == email and w.User_role == 'staff':
                messages.success(request, 'You have already registered..Please login')
                return render(request, 'register_staff.html')
        psw = request.POST.get('psw')
        user_name = request.POST.get('user_name')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)

        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return render(request, 'register_staff.html')

        user = User.objects.create_user(username=user_name, email=email, password=psw)
        user.save()

        reg = Registration()
        reg.First_name = first_name
        reg.Last_name = last_name
        reg.Email = email
        reg.Password = psw
        reg.Registration_date = y
        reg.Image = photo
        reg.About_website = 'Nil'
        reg.User_role = typ
        reg.user = user
        reg.save()
        messages.success(request, 'You have successfully registered')
        return redirect('home')
    else:
        return render(request, 'register_staff.html')


def register_user(request):
    if request.method == 'POST':
        x = datetime.datetime.now()
        y = x.strftime("%Y-%m-%d")
        typ = request.POST.get('user')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mgn = Registration.objects.all()
        for w in mgn:
            if w.Email == email and w.User_role == 'user':
                messages.success(request, 'You have already registered..Please login')
                return render(request, 'register_user.html')
        psw = request.POST.get('psw')
        user_name = request.POST.get('user_name')

        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return render(request, 'register_user.html')

        user = User.objects.create_user(username=user_name, email=email, password=psw)
        user.save()

        reg = Registration()
        reg.First_name = first_name
        reg.Last_name = last_name
        reg.Email = email
        reg.Password = psw
        reg.Registration_date = y
        reg.About_website = 'Nil'
        reg.User_role = typ
        reg.user = user
        reg.save()
        messages.success(request, 'You have successfully registered')
        return redirect('home')
    else:
        return render(request, 'register_user.html')


def register_admin(request):
    if request.method == 'POST':
        lk = Registration.objects.all()
        for t in lk:
            if t.User_role == 'admin':
                messages.success(request, 'You are not allowed to be registered as admin')
                return redirect('home')
        x = datetime.datetime.now()
        z = x.strftime("%Y-%m-%d")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        fs = FileSystemStorage()
        admin = request.POST.get('admin1')
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.Email == email:
                messages.success(request, 'User already exists')
                return render(request, 'register_admin.html')

        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return render(request, 'register_admin.html')

        user = User.objects.create_user(username=user_name, email=email, password=psw)
        user.save()

        t = Registration()
        t.First_name = first_name
        t.Last_name = last_name
        t.Email = email
        t.Password = psw
        t.Registration_date = z
        t.About_website = 'Nil'
        t.User_role = admin
        t.user = user
        t.save()
        messages.success(request, 'You have successfully registered as admin')
        return redirect('home')
    else:
        return render(request, 'register_admin.html')

def logout(request):
    auth.logout(request)
    return redirect('home')


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html')
        auth_login(request, user)
        reg = Registration.objects.filter(user=user, Password=password).first()
        if reg:
            if reg.User_role == 'admin':
                request.session['login'] = reg.id
                return redirect('admin_home1')
            elif reg.User_role == 'staff':
                request.session['login'] = reg.id
                request.session['staff'] = reg.Email
                return redirect('staffhome')
            elif reg.User_role == 'user':
                request.session['login'] = reg.id
                return redirect('userhome')
        else:
            messages.error(request, 'Username or password entered is incorrect')
            return render(request, 'login.html')
    return render(request, 'login.html')


def userhome(request):
    if request.method == 'POST':        
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity -1
                else:
                    cart[product] = quantity +1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print(request.session['cart'])
        return redirect('userhome')
    else:
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = Product.get_all_products()
        if 'cart' not in request.session:
            request.session['cart'] = {}
        return render(request, 'user_home.html',{'prds': products, 'cart': request.session['cart']})




def staffhome(request):
    return render(request, 'staff_home.html')


def admin_home1(request):
    return render(request, 'adminhome1.html')

def cart(request):
    ids = list(request.session.get('cart').keys())
    products = Product.get_products_id(ids)
    print(products)
    return render(request,'cart.html', {'productcart': products })



@login_required
def checkout(request):
    if request.method == 'POST':    
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        user = request.user
        registration = user.registration
        cart = request.session.get('cart')
        products = Product.get_products_id(list(cart.keys()))
        print(address , phone , pincode , user , cart , products )
        for product in products:
            order = Order(user = registration,
                          product = product,
                          price = product.price,
                          address = address ,
                          pincode = pincode ,
                          phone = phone,
                          quantity = cart.get(product.name))
            order.placeorder();
        request.session['cart'] ={}
        return redirect('orderview')
    return render(request, 'checkout.html')

def orderview(request):
    user = request.user
    registration = user.registration
    orders = Order.get_orders_by_user(registration)
    print(orders)
    orders = orders.reverse()
    return render (request, 'orders.html' , { 'orders': orders })


def block(request):
    u_reg = Registration.objects.filter(Q(User_role="user") | Q(User_role="user_blocked"))
    return render(request,'block.html',{'u_reg':u_reg})

def blocks(request, id):
    klk = Registration.objects.get(id=id)
    klk.User_role = 'user_blocked'
    klk.save()
    u_reg = Registration.objects.filter(Q(User_role="user") | Q(User_role="user_blocked"))
    return render(request,'block.html',{'u_reg':u_reg})


def allows(request, id):
    klk = Registration.objects.get(id=id)
    klk.User_role = 'user'
    klk.save()
    u_reg = Registration.objects.filter(Q(User_role="user") | Q(User_role="user_blocked"))
    return render(request, 'block.html', {'u_reg': u_reg})


def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)
        description = request.POST['description']
        image = request.FILES.get('image', None)
        Product.objects.create(
        name=name,
        price=price,
        category=category,
        description=description,
        image=image
        )
        return redirect('product_list')
    categories = Category.objects.all()
    return render(request, 'add_prds.html', {'categories': categories})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def remove_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('product_list')


def order_details(request):
    orders = Order.objects.all()
    return render(request, 'order_details.html', {'orders': orders})


def order_views(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_views.html', {'order': order})

def change_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = OrderStatusForm(request.POST or None, instance=order)
    if form.is_valid():
        form.save()
        return redirect('order_details', order_id=order_id)
    return render(request, 'change_status.html', {'form': form, 'order': order})

def user_details(request):
    users = Registration.objects.all()
    context = {'users': users}
    return render(request, 'user_details.html', context)

def usercontact(request):
    return render(request, 'usercontact.html')

def userblog(request):
    return render(request, 'userblog.html')