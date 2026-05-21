from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.CartView.as_view(), name="cart"),
    path("items/", views.CartItemView.as_view(), name="cart_item_add"),
    path("items/<int:sku_id>/", views.CartItemView.as_view(), name="cart_item_update"),
    path("select-all/", views.CartSelectAllView.as_view(), name="cart_select_all"),
    path("remove-selected/", views.CartRemoveSelectedView.as_view(), name="cart_remove_selected"),
]
