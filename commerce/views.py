from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Category, Product, User, Cart, CartItem, UserProfile
from .forms import ProductForm, LoginForm, RegisterForm, UserProfileForm
from decimal import Decimal
from django.contrib.auth.forms import UserCreationForm
from .permission import AdminRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  
            login(request, user)  
            return redirect('/')  

        return render(request, 'user/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
       
        if request.user.is_authenticated:
            return redirect('home')  

        form = AuthenticationForm()
        return render(request, 'user/login.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')  # Foydalanuvchi allaqachon tizimga kirgan bo'lsa / If user has already used web

        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')  # Tizimga kirganidan keyin home sahifasiga yo'naltirish / after enterin direct to home page

        return render(request, 'user/login.html', {'form': form})

            
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')            
                       



# Home View
class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user, is_active=True).first()
        else:
            cart_id = request.session.get('cart_id')
            if cart_id:
                cart = Cart.objects.filter(id=cart_id, is_active=True).first()
            else:
                cart = None
        
        cart_count = cart.items_count() if cart else 0  # Savatchadagi itemlar soni
        categories = Category.objects.all()
        products=Product.objects.all()

        return render(request, 'user/home.html', {
            "cart_count": cart_count,  # cart_count ni taqdim etish
            "categories": categories,
            "products": products,
        })

    

class CategoryView(View):
    def get(self, request, id):
        category = get_object_or_404(Category, id=id)  
        products = Product.objects.filter(category=category)  
        categories = Category.objects.all()

        return render(request, 'user/home.html', {
            'category': category,
            'products': products,
            'categories': categories
        })
 
# VIEW 
    


class ProductView(View):
    def get(self, request, category_slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.all()

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        context = {
            'category': category,
            'products': products,
            'categories': categories,
        }
        return render(request, 'user/home.html', context)


### PRODUCT_DETAILVIEW    


class ProductDetailView(View):
    
    def get(self, request, pk):
        cart = None  # Cart ni oldindan None qilamiz
        cart_id = request.session.get('cart_id', None)  # Cart ID ni sessiondan olamiz
        
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user, is_active=True).first()
        
        if not cart and cart_id:  # Agar foydalanuvchi cart'ga ega bo'lmasa, sessiondan qidiramiz
            cart = Cart.objects.filter(id=cart_id, is_active=True).first()
            
        cart_count = cart.items_count() if cart else 0
        product = get_object_or_404(Product, id=pk)   
        categories = Category.objects.all()
        
        return render(request, 'user/about.html', {
            "cart_count": cart_count,
            "product": product,
            "categories": categories
        })  

        
### PRODUCT_CREATEVIEW

class ProductCreateView(AdminRequiredMixin,View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'user/product_form.html', {"form": form})
    
    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.price = round(Decimal(new_product.price), 2)
            new_product.save()
            return redirect('home')  
        return render(request, 'user/product_form.html', {"form": form})  

## UPDATE PRODUCT VIEW
    
class UpdateProductView(AdminRequiredMixin,View):
    
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        return render(request, 'user/product_form.html', {"form": form, "product": product})     
    
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            updated_product = form.save(commit=False)
            updated_product.price = round(Decimal(updated_product.price), 2)
            updated_product.save()
            return redirect('home')
        return render(request, 'user/product_form.html', {"form": form, "product": product}) 
## DELETE PRODUCT

class DeleteProductView(AdminRequiredMixin,View):
    def get(self, request, pk):
        product=get_object_or_404(Product, pk=pk)
        return render(request, 'user/delete_confirm.html', {"product":product})
    def post(self, request, pk):
        product=get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect('home')
    
    
## Search View 

class SearchView(View):
    def get(self, request):
        categories=Category.objects.all
        query=request.GET.get('q', '')    
        result=Product.objects.filter(name__icontains=query)
        return render(request, 'user/home.html', {"products":result, "query":query, "categories":categories})
    
    
    

### Cart View 

class AddCartView(View):
    def get_cart(self, request):
        """ Foydalanuvchi sessiyasi yoki tizimga kirganligini tekshirib, savatchani qaytaradi """
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        else:
            cart_id = request.session.get('cart_id')
            if cart_id:
                cart = Cart.objects.filter(id=cart_id, is_active=True).first()
            else:
                cart = Cart.objects.create(is_active=True)
                request.session['cart_id'] = cart.id
        return cart

    def post(self, request, product_id):
        """ Savatchaga mahsulot qoshish (POST usuli) """
        product = get_object_or_404(Product, id=product_id)
        cart = self.get_cart(request)  # self.get_cart(request) ishlatish kerak

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('cart_view')  # Savatcha ko‘rinishi uchun redirect


            
class CartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user, is_active=True).first()  
        else:
            cart_id = request.session.get('cart_id')
            if cart_id:
                cart = Cart.objects.filter(id=cart_id, is_active=True).first()
            else:
                cart = None

        cart_items = cart.items.all() if cart else []
        total_price = cart.total_price() if cart else 0 
        items_count = cart.items_count() if cart else 0
        categories = Category.objects.all()

        return render(request, 'user/cart.html', {
            "cart_items": cart_items,
            "total_price": total_price,
            "items_count": items_count,
            "categories": categories,
            "cart_count": items_count,  # cart_count ni tekshirib, shu qiymatni yuboring
        })
class RemoveCartView(View):
    def get(self, request, product_id):
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user, is_active=True).first()
        else:
            cart_id = request.session.get('cart_id')
            if cart_id:
                cart = Cart.objects.filter(id=cart_id, is_active=True).first()
            else:
                cart = None  # Savatcha bo'lmasa, cart bo'lmaydi

        if cart:
            try:
                cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
                cart_item.delete()
            except CartItem.DoesNotExist:
                pass

        return redirect('cart_view')
    
### Profile View    


class ProfileView(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile, created = UserProfile.objects.get_or_create(user=user)
       
        
        
        return render(request, 'user/profile.html', {
            'user':user,
            'profile':profile,
            
            
        })
        
        
class EditProfileView(View):
    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(instance=profile)
        return render(request, 'user/profile_edit.html', {
            'form':form,
            'profile':profile
        })
        
    def post(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)    
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
        return render(request, 'user/edit_profile.html', {
            'form':form,
            'profile':profile
        })
        
            