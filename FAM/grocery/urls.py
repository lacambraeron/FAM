from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products", views.products, name="products"),
    path("menu", views.menu, name="menu"),
    path("categories/<int:category_id>", views.category, name="category"),
    path("create", views.create, name="create"),
    path("item/<int:item_id>", views.item, name="item"),
    path("item/<int:item_id>/review", views.review, name="review"),
    path('edit-item/<int:item_id>/', views.edit_item, name='edit_item'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("history/<int:user_id>", views.history, name="history"),
    path("search", views.search, name="search"),
    path("add-to-cart/<int:item_id>", views.add_to_cart, name="add_to_cart"),
    path("update-cart-item/<int:cart_item_id>", views.update_cart_item, name="update_cart_item"),
    path("cart", views.view_cart, name="cart"),
    path("review_order", views.revieworder, name="review_order"),
    path("remove-from-cart/<int:cart_item_id>", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("order", views.order, name="order"),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
]
