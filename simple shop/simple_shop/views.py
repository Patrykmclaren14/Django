from .models import Cart, Product
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from os import error
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from numpy import product
from .models import Product, Cart
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum


def registration_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Sprawdzenie, czy hasła są identyczne
        if password1 != password2:
            # Wysłanie komunikatu o błędzie
            error_message = 'Passwords do not match.'
            return render(request, 'register.html', {'error_message': error_message})

        # Sprawdzenie, czy użytkownik o podanej nazwie już istnieje
        if User.objects.filter(username=username).exists():
            # Wysłanie komunikatu o błędzie
            error_message = 'Username already exists.'
            return render(request, 'register.html', {'error_message': error_message})

        # Utworzenie nowego użytkownika
        user = User.objects.create_user(
            username=username, email=email, password=password1)
        user.save()

        # Przekierowanie użytkownika na stronę logowania
        return redirect('login')    # Wyświetlenie formularza rejestracji
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
            # Zalogowano użytkownika, przekieruj gdzieś
        else:
            error_message = "User doesn't exit"
            # Niepoprawne dane logowania, wyświetl błąd
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        user = request.user

        product = Product.objects.create(
            name=name, price=price, description=description, user=user)
        product.save()
    return render(request, 'add_product.html', {})


def profile(request, user_id):
    users = User.objects.get(pk=user_id)
    return render(request, 'profile.html', {'users': users})


def profile_page(request, user_id):
    user = User.objects.get(pk=user_id)
    products = Product.objects.all()

    return render(request, 'profile_page.html', {'user': user, 'products': products})


def edit_profile(request, user_id):
    if request.method == 'POST':
        # Pobranie danych z formularza
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        # Pobranie aktualnego użytkownika
        user = User.objects.get(pk=user_id)

        # Aktualizacja danych użytkownika
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Zalogowanie użytkownika po zmianie danych
        user = authenticate(username=username)
        if user is not None:
            login(request, user)
            user = User.objects.get(pk=user_id)

        # Przekierowanie użytkownika na stronę profilu
        return redirect('home')

    # Wyświetlenie formularza z danymi użytkownika
    user = User.objects.get(pk=user_id)
    return render(request, 'edit_profile.html', {'user': user})


def users_page(request):
    users_2 = Paginator(User.objects.all(), 4)
    page_number = request.GET.get('page')
    users = users_2.get_page(page_number)

    return render(request, 'users_page.html', {'users': users, 'users_2': users_2})


def show_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'show_product.html', {'product': product})


def cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = Product.objects.get(pk=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.products.add(product)
        message = "Product added successfully"
    else:
        cart, created = Cart.objects.get_or_create(user=request.user)
        message = None
    cart_total = cart.products.aggregate(Sum('price'))['price__sum']
    return render(request, 'cart.html', {'cart': cart, 'cart_total': cart_total, 'message': message})
