# models.py
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/images/products', null=True, blank=True)


    def __str__(self):
        return self.name

class CarouselImage(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='static/images/carousel')



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Calculate the total price before saving
        self.total_price = Decimal(self.quantity) * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} for {self.user.username}'
    

# user details 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    address = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

# Order details

class Order(models.Model):
    DELIVERED = 'Delivered'
    NOT_DELIVERED = 'Not Delivered'
    
    STATUS_CHOICES = [
        (DELIVERED, 'Delivered'),
        (NOT_DELIVERED, 'Not Delivered'),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    phone_number = models.TextField(max_length=10 , blank=True)
    quantity = models.PositiveIntegerField(default=1)
    date = models.DateField(auto_now_add=True) 
    total = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=NOT_DELIVERED,
    )

    def save(self, *args, **kwargs):
        # Calculate total price based on the product price and quantity
        self.total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username} for {self.product.name} on {self.date}"
