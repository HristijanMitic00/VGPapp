from django.contrib import admin
from .models import Game, Order, GameInOrder, GameInCart, Cart


# Register your models here.

class GameAdmin(admin.ModelAdmin):
    list_display = ("pk","name", "created_at", "game_category", "user")
    list_filter = ("name", "created_at")
    search_fields = ("name", "game_category")

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return obj is not None and obj.user == request.user

    def has_change_permission(self, request, obj=None):
        return obj is not None and obj.user == request.user

    def has_view_permission(self, request, obj=None):
        return True


class OrderAdmin(admin.ModelAdmin):
    list_display = ("pk","user", "created_at")
    search_fields = ("user__username",)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return obj is not None and obj.user == request.user

    def has_change_permission(self, request, obj=None):
        return obj is not None and (obj.user == request.user or request.user.is_superuser)

    def has_view_permission(self, request, obj=None):
        return True


class GameInOrderAdmin(admin.ModelAdmin):
    list_display = ("order_id","order", "game", "quantity")
    search_fields = ("order__user__username", "game__name")

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return obj is not None and request.user is not None

    def has_change_permission(self, request, obj=None):
        return obj is not None and request.user is not None

    def has_view_permission(self, request, obj=None):
        return True


class GameInCartAdmin(admin.ModelAdmin):
    list_display = ("cart_id","cart", "game", "quantity")
    search_fields = ("cart__user__username", "game__name")

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return obj is not None and request.user is not None

    def has_change_permission(self, request, obj=None):
        return obj is not None and request.user is not None

    def has_view_permission(self, request, obj=None):
        return True


class CartAdmin(admin.ModelAdmin):
    list_display = ("pk","user", "created_at")
    search_fields = ("user__username", "games__name")

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return obj is not None and obj.user == request.user

    def has_change_permission(self, request, obj=None):
        return obj is not None and obj.user == request.user

    def has_view_permission(self, request, obj=None):
        return True


admin.site.register(Game, GameAdmin)
admin.site.register(GameInCart, GameInCartAdmin)
admin.site.register(GameInOrder, GameInOrderAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
