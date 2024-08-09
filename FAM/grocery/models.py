from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Item(models.Model):
    active = models.BooleanField(default=True)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('item', kwargs={'item_id': self.pk})
    
class Review(models.Model):
    content = models.TextField(blank=True)
    reviewer = models.ForeignKey("User", on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.content
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_method = models.CharField(max_length=20, choices=[("delivery", "Delivery"), ("pickup", "Pickup")], default="delivery")
    recipient_first = models.CharField(max_length=20, default="", null=True, blank=True)
    recipient_middle = models.CharField(max_length=20, default="", null=True, blank=True)
    recipient_last = models.CharField(max_length=20, default="", null=True, blank=True)
    recipient_address = models.CharField(max_length=50, default="", null=True, blank=True)
    recipient_city = models.CharField(max_length=20, default="", null=True, blank=True)
    recipient_state = models.CharField(max_length=15, default="", null=True, blank=True)
    recipient_zip = models.IntegerField(default=0, null=True, blank=True)  # You can set a default ZIP code here
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("fulfilled", "Fulfilled"), ("cancelled", "Cancelled")], default="pending")

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=19, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item.title} for Order #{self.order.id}"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart", blank=True, null=True)
    session_key = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Cart for {self.user.username if self.user else 'Guest'}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.title} in Cart #{self.cart.id}"
