from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, Order, Product, CarouselImage


# Create your views here.

# index view
def index(request):
    products = Product.objects.all()
    carousel_images = CarouselImage.objects.all()
    return render(request, 'index.html', {'products': products, 'carousel_images': carousel_images})

# contact view
def contact(request):
    return render(request, 'contact.html')

# product view
def product(request):
    return render(request, 'product.html')

# profile view
@login_required(login_url='/login/')
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    return render(request, 'profile.html',{'user':user , "orders":orders})




# Authentication handling

# signup user 
def signupuser(request):
    if request.method == 'POST':
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password") 

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect("signup")
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect("signup")
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        messages.success(request, 'Your account has been create successfully!')
        return redirect("/")
    return render(request, "signup.html")

# login user view
def loginUser(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully!') 
            return redirect("/")
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect("login")
    return render(request, "login.html")

# logout user view
@login_required(login_url='/login/')
def logoutUser(request):
        logout(request)
        messages.success(request, 'You have been logged out successfully!')

        return redirect("/")






# shop view
def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})

# productdetails view
def productdetails(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'productdetails.html', {'product': product})

# # buy view
@login_required(login_url='/login/')
def buy(request, product_id=None):
    if request.method == 'POST':
        messages.info(request,"reached post method")
        full_name = request.POST.get('fullName')
        phone_number = request.POST.get('phone')
        address = request.POST.get('address')

        if product_id: 
             # If a single product ID is provided
            product = get_object_or_404(Product, id=product_id)
            # Create the order object for a single product
            order = Order.objects.create(
                user=request.user,
                product=product,  # Associate the product with the order
                full_name=full_name,
                phone_number=phone_number,
                shipping_address=address
            )
            messages.success(request, 'Order placed successfully!')
        else:  # If no single product ID is provided (i.e., multiple products from the cart)
            cart_items = Cart.objects.filter(user=request.user)
            if not cart_items:
                messages.info(request, 'Your cart is empty. Please add items to your cart first.')
                return redirect('shop')  # Redirect to the shop section if the cart is empty

            for cart_item in cart_items:
                # Create an order object for each product in the cart
                order = Order.objects.create(
                    user=request.user,
                    product=cart_item.product,  # Associate the product with the order
                    full_name=full_name,
                    quantity = cart_item.quantity,
                    phone_number=phone_number,
                    shipping_address=address
                )
                cart_item.delete()
            messages.success(request, 'Orders placed successfully!')

        return redirect('profile')  # Redirect to the user's profile page after placing the order
    else:
        # If it's a GET request, render the buy.html template
        if product_id:  # If a single product ID is provided
            product = get_object_or_404(Product, id=product_id)
            return render(request, 'buy.html', {'product': product})
        else:  # If no single product ID is provided (i.e., multiple products from the cart)
            return render(request, 'buy.html')


# cart view
@login_required(login_url='/login/')
def cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    cart_total = sum(item.total_price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})

# add to cart view
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        # Check if the product is already in the user's cart
        cart_item = Cart.objects.filter(user=request.user, product=product).first()

        if cart_item:
            # If the product is already in the cart, increase the quantity
            cart_item.quantity += 1
            cart_item.save()
        else:
            # If the product is not in the cart, create a new cart item
            Cart.objects.create(user=request.user, product=product)

        messages.success(request, f'{product.name} added to your cart.')
    else:
        # User is not authenticated, redirect to login page
        messages.info(request, 'Please log in to add items to your cart.')
        return redirect('login')

    return redirect('cart')

# remove from cart view
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)

    # check if the item is more than one
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    messages.success(request, f'{cart_item.product.name} removed from your cart.')
    return redirect('cart')