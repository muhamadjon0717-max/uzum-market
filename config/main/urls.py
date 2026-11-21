
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add_product, name="add_product"),
    path("edit/<int:pk>/", views.edit_product, name="edit_product"),
    path("delete/<int:pk>/", views.delete_product, name="delete_product"),
    path("add-cart/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("remove-cart/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/", views.cart, name="cart"),
]
