from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (CategoryView, ProductView, ProductDetailView, ProductCreateView, HomeView,
UpdateProductView, DeleteProductView, LoginView, LogoutView, RegisterView, SearchView, AddCartView, CartView, RemoveCartView,
ProfileView    )

# app_name


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),


    path('', HomeView.as_view(), name='home'),
    path('category/<int:id>/', CategoryView.as_view(), name='category'),
    
    ## Product CRUD
    
    path('product/<slug:category_slug>/', ProductView.as_view(), name='product'),
    path('about/<int:pk>/', ProductDetailView.as_view(), name='about'),
    path('product/create', ProductCreateView.as_view(), name='product_create'),
    
    path('product/update/<int:pk>/', UpdateProductView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', DeleteProductView.as_view(), name='product_delete'),
    
    path('search/', SearchView.as_view(), name='search'),
    
    path('add_cart/<int:product_id>', AddCartView.as_view(), name='add_cart'),
    path('cart_view/', CartView.as_view(), name='cart_view'),
    path('remove_cart/<int:product_id>', RemoveCartView.as_view(), name='remove_cart'),
   
   ### Profile Url
    
    path('profile/<str:username>/',ProfileView.as_view(), name='profile' )
  
   
    
    
]

