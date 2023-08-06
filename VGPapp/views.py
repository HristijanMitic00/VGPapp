from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import GameForm, AddGameToCartForm, OrderForm, NewUserForm
from .models import Game, GameInCart, GameInOrder, Cart, Order


# Create your views here.

def index(request):
    queryset = Game.objects.all()
    paginator = Paginator(queryset, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"games": queryset, "Date": datetime.now().date(), "form": GameForm, "page_obj": page_obj}
    return render(request, "index.html", context=context)


def details(request, name):
    game = Game.objects.get(name=name)
    context = {"game": game, "form": AddGameToCartForm}
    return render(request, "details.html", context=context)


@login_required
def add(request):
    if request.method == "POST":
        form_data = GameForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            game = form_data.save(commit=False)
            game.user = request.user
            game.image = form_data.cleaned_data['image']
            game.save()
            return redirect("index")

    return render(request, "add.html", context={"form": GameForm})


@login_required
def cart(request):
    if not request.user.is_authenticated:
        return redirect("login")

    cart, createdCart = Cart.objects.get_or_create(user=request.user)
    games = Cart.objects.get_or_create(user=request.user)[0].gameincart_set.all()
    context = {"games": games, "cart": cart}

    return render(request, "cart.html", context)


@login_required
def add_to_cart(request, name):
    if not request.user.is_authenticated:
        return redirect("login")

    cart, createdCart = Cart.objects.get_or_create(user=request.user)
    if createdCart:
        cart.totalPrice = 0
    game = Game.objects.get(name=name)
    game_in_cart, created = GameInCart.objects.get_or_create(
        cart=cart, game=game
    )

    if created:
        game_in_cart.quantity = 1
        cart.totalPrice += game.price
    else:
        game_in_cart.quantity += 1
        cart.totalPrice += game.price

    cart.save()

    game_in_cart.save()

    return redirect("index")


@login_required
def remove_cart(request):
    if not request.user.is_authenticated:
        return redirect("login")

    cart = Cart.objects.get(user=request.user)

    if cart is not None:
        cart.totalPrice = 0
        cart.delete()

    return redirect("index")


@login_required
def remove_from_cart(request, name):
    if not request.user.is_authenticated:
        return redirect("login")

    cart = Cart.objects.get_or_create(user=request.user)[0]
    game = Game.objects.get(name=name)

    game_in_cart = GameInCart.objects.get(cart=cart, game=game)

    if game_in_cart is not None:
        cart.totalPrice -= game_in_cart.game.price * game_in_cart.quantity
        cart.save()
        game_in_cart.delete()

    return redirect("cart")


@login_required
def checkout(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        form_data = OrderForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            order = form_data.save(commit=False)
            order.user = request.user
            cartT = Cart.objects.get(user=request.user)
            cart = Cart.objects.get_or_create(user=request.user)[0].gameincart_set.all()
            order.totalPrice = cartT.totalPrice
            order.save()
            for game_in_cart in cart:
                game_in_order = GameInOrder.objects.create(
                    order=order,
                    game=game_in_cart.game,
                    quantity=game_in_cart.quantity,
                )
                game_in_order.save()
                game_in_cart.delete()

            cart.delete()
            cartT.delete()

            return redirect("success")

    cart = Cart.objects.get_or_create(user=request.user)[0].gameincart_set.all()
    context = {"cart": cart, "form": OrderForm}

    return render(request, "checkout.html", context)


def success(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "successfulOrder.html")


@login_required
def userOrders(request):
    if not request.user.is_authenticated:
        return redirect("login")

    queryset = Order.objects.filter(user=request.user)

    context = {"orders": queryset}

    return render(request, "userOrders.html", context)


@login_required
def checkOrder(request, id):
    if not request.user.is_authenticated:
        return redirect("login")

    order = Order.objects.get(id=id)
    games = order.gameinorder_set.all()

    context = {"order": order, "games": games}

    return render(request, "orderInfo.html", context)


@login_required
def userInfo(request):
    if not request.user.is_authenticated:
        return redirect("login")

    user = User.objects.get(username=request.user.username)

    context = {"user": user}

    return render(request, "userInfo.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    context = {"form": form}
    return render(request, "registration/register.html", context)
