from django import forms
from .models import Game, GameInCart, Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class GameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Game
        exclude = ("user", "created_at", "updated_at")


class AddGameToCartForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddGameToCartForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = GameInCart
        exclude = ("game", "cart")


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Order
        exclude = ("user", "games", "updated_at", "created_at", "order_state", "totalPrice")


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
