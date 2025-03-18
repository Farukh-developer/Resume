from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ADMIN = 'admin'
    CLIENT = 'client'
    USER_ROLE_CHOICES = {
        ("client", "client"),
        ("admin", "admin"),
    }
    image = models.ImageField(upload_to='product/', null=True, blank=True, default="product/default.jpeg")
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    user_role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES, default="client")


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    profile_pict = models.ImageField(upload_to='product/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)


class Category(models.Model):
    name=models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)    
    image=models.ImageField(upload_to='product/')
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    
    def __str__(self):
        return self.name
    
    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True) 
    def __str__(self):
        return f"Cart {self.id} for {self.user if self.user else 'Guest'}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    
    def items_count(self):  # ✅ Agar sizga items soni kerak bo'lsa, metod qo‘shing
        return self.items.count()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
