import decimal

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.db.models import F, Sum

from .models import Order, OrderItem, Category, Review, Item, User, Cart, CartItem


class CreateItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'image_url', 'category', 'price']

    def __init__(self, *args, **kwargs):
        super(CreateItemForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

class UpdateCartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'image_url', 'category', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
        }

# Define a custom function to check if the user is the specific admin
def is_specific_admin(user):
    # Check if the user is authenticated and is an admin
    return user.is_authenticated and user.is_admin

def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    items = Item.objects.filter(active=True, category=category).order_by("-creation_time").all()
    return render(request, "grocery/index.html", {
        "title": f"Items in {category.name}",
        "items": items
    })


@login_required
def review(request, item_id):
    if request.method == "POST":
        content = request.POST["comment"]
        item = get_object_or_404(Item, pk=item_id)
        comment = Review(reviewer=request.user, content=content, item=item)
        comment.save()
        return HttpResponseRedirect(reverse("item", args=(item.id,)))

@login_required
@user_passes_test(is_specific_admin)
def create(request):
    if request.method == "POST":
        form = CreateItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "grocery/create.html", {
                "form": form
            })
    else:
        return render(request, "grocery/create.html", {
            "form": CreateItemForm()
        })


def products(request):
    items = Item.objects.filter(category__name="Grocery").order_by("-title").all()
    return render(request, "grocery/products.html", {
        "title": "Products",
        "items": items
    })

def menu(request):
    items = Item.objects.filter(category__name="Restaurant").order_by("title").all()
    return render(request, "grocery/menu.html", {
        "title": "Menu",
        "items": items
    })

def index(request):
    return render(request, "grocery/index.html")


def item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    reviews = item.comments.order_by("-creation_time").all()
    return render(request, "grocery/item.html", {
        "reviews": reviews,
        "item": item
    })
    
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication is successful
        if user is not None:
            login(request, user)
            
            # Transfer items from session-based cart to user's cart
            session_cart = Cart.objects.filter(session_key=request.session.session_key).first()
            if session_cart:
                session_cart.user = user
                session_cart.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "grocery/login.html", {"message": "Invalid username and/or password."})
    else:
        return render(request, "grocery/login.html")


def logout_view(request):
    # Clear session-based cart
    Cart.objects.filter(session_key=request.session.session_key).delete()
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def history(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    orders = Order.objects.filter(user=user).order_by("created_at")

    for order in orders:
        # Fetch related order items for each order
        order_items = OrderItem.objects.filter(order=order)
        order.items = order_items  # Attach order items to the order object

    return render(request, "grocery/history.html", {
        "title": "Order History",
        "orders": orders,
        "user": user,
    })

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "grocery/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "grocery/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "grocery/register.html")

def search(request):
    query = request.GET.get('q')
    if query:
        # Perform a case-insensitive search for items containing the query
        items = Item.objects.filter(title__icontains=query)

        # If exact match found, redirect to item page
        exact_match = items.filter(title__iexact=query).first()
        if exact_match:
            return HttpResponseRedirect(exact_match.get_absolute_url())
        else:
            # If no exact match found, display items containing the query
            return render(request, "grocery/products.html", {
                "title": f"Search results for '{query}'",
                "items": items
            })
    else:
        message = "Error: Input a keyword"
        return render(request, "grocery/products.html", {
            "message": message
        })

def add_to_cart(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Try to get the cart associated with the user
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            # If no cart exists, create a new one
            cart = Cart.objects.create(user=request.user)
            # Delete any existing carts associated with the session
            Cart.objects.filter(session_key=request.session.session_key).delete()
    else:
        # Try to get the cart associated with the session
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
        if not cart:
            # If no cart exists, create a new one
            cart = Cart.objects.create(session_key=request.session.session_key)
            # Delete any existing carts associated with the user
            Cart.objects.filter(user=request.user).delete()

    # Check if the item is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

    # Increase quantity if item is already in the cart
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return HttpResponseRedirect(reverse("cart"))


def view_cart(request):
    # Get the current session key
    session_key = request.session.session_key

    if request.user.is_authenticated:
        # If user is authenticated, get their cart
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        # Clear any session-based cart associated with the user
        Cart.objects.filter(session_key=session_key, user=request.user).delete()
    else:
        # If user is not authenticated, get or create session-based cart
        cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
    
    total_price = cart.items.annotate(
        item_total=F('item__price') * F('quantity')
    ).aggregate(
        total=Sum('item_total')
    )['total'] or 0
    return render(request, "grocery/cart.html", 
        {"cart": cart,
         "total_price": total_price})

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()

    return HttpResponseRedirect(reverse("cart"))

def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    
    if request.method == 'POST':
        form = UpdateCartItemForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            return redirect('cart')
    
    # Handle invalid form or non-POST request
    return redirect('view_cart')

def revieworder(request):
        # Get the current session key
    session_key = request.session.session_key

    if request.user.is_authenticated:
        # If user is authenticated, get their cart
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        # Clear any session-based cart associated with the user
        Cart.objects.filter(session_key=session_key, user=request.user).delete()
    else:
        # If user is not authenticated, get or create session-based cart
        cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
    
    total_price = cart.items.annotate(
        item_total=F('item__price') * F('quantity')
    ).aggregate(
        total=Sum('item_total')
    )['total'] or 0
    return render(request, "grocery/revieworder.html", 
        {"cart": cart,
         "total_price": total_price})
    

def checkout(request):
    # Get the current session key
    session_key = request.session.session_key
    
    # Initialize cart to None
    cart = None
    
    if request.method == "GET":
        if request.user.is_authenticated:
            # If user is authenticated, get their cart
            cart, _ = Cart.objects.get_or_create(user=request.user)
            # Clear any session-based cart associated with the user
            Cart.objects.filter(session_key=session_key, user=request.user).delete()
        else:
            # If user is not authenticated, get or create session-based cart
            cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
        
        # Calculate total items and total price for rendering the form
        total_items = sum(item.quantity for item in cart.items.all())
        total_price = sum(item.item.price * item.quantity for item in cart.items.all())

        return render(request, "grocery/checkout.html", 
                      {"title": "Checkout",
                       "cart": cart,
                       "total_items": total_items,
                       "total_price": total_price})
        
    elif request.method == "POST":
        # Retrieve form data and create order
        delivery_method = "delivery"
        recipient_first = request.POST.get("recipient_first")
        recipient_middle = request.POST.get("recipient_middle")
        recipient_last = request.POST.get("recipient_last")
        recipient_address = request.POST.get("recipient_address")
        recipient_city = request.POST.get("recipient_city")
        recipient_state = request.POST.get("recipient_state")
        recipient_zip = request.POST.get("recipient_zip")

        # Create order instance
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            delivery_method=delivery_method,
            recipient_first=recipient_first,
            recipient_middle=recipient_middle,
            recipient_last=recipient_last,
            recipient_address=recipient_address,
            recipient_city=recipient_city,
            recipient_state=recipient_state,
            recipient_zip=recipient_zip
        )
        
        # Retrieve cart items and create order items
        if request.user.is_authenticated:
            # If user is authenticated, get their cart
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            # If user is not authenticated, get or create session-based cart
            cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
        
        cart_items = cart.items.all()
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                item=cart_item.item,
                quantity=cart_item.quantity,
                price=cart_item.item.price
            )
        
        # Delete the cart after creating the order
        cart.delete()
        
        # Redirect to a confirmation page
        return redirect("index")


def edit_item(request, item_id):
    # Get the item object based on the item_id
    item = get_object_or_404(Item, pk=item_id)
    
    if request.method == "POST":
        # If the form is submitted with POST data, process the form
        form = EditItemForm(request.POST, instance=item)
        if form.is_valid():
            # If the form data is valid, save the changes to the item object
            form.save()
            # Redirect to the item page after editing
            return redirect('item', item_id=item_id)
    else:
        # If the request is GET, initialize the form with the current item data
        form = EditItemForm(instance=item)
    
    # Render the edit item page with the form
    return render(request, 'grocery/edit_item.html', {'form': form})

@login_required
def order(request):
    # Retrieve orders for the current user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'grocery/history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'grocery/order_detail.html', {'order': order})