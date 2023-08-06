from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Game(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to="games/")
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Action = "Action"
    Sport = "Sport"
    Horror = "Horror"
    Cooking = "Cooking"
    Puzzle = "Puzzle"
    GAME_CATEGORY = [
        (Action, "Action"),
        (Sport, "Sport"),
        (Horror, "Horror"),
        (Cooking, "Cooking"),
        (Puzzle, "Puzzle"),
    ]
    game_category = models.CharField(
        max_length=20,
        choices=GAME_CATEGORY,
        default=Action)

    class Meta:
        ordering = ("name", "price", "created_at")

    def __str__(self):
        return self.name + " " + self.user.first_name


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    games = models.ManyToManyField(to=Game, through="GameInCart")
    totalPrice = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}"


class GameInCart(models.Model):
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.game.name} {self.quantity}"


class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    games = models.ManyToManyField(to=Game, through="GameInOrder")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Ordered = "Ordered"
    Delivered = "Delivered"
    ORDER_STATE = [
        (Ordered, "Ordered"),
        (Delivered, "Delivered")
    ]
    order_state = models.CharField(
        max_length=20,
        choices=ORDER_STATE,
        default=Ordered)
    buyerName = models.CharField(max_length=50)
    delivery_address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=100)
    totalPrice = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user}"


class GameInOrder(models.Model):
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.game.name} {self.quantity}"
