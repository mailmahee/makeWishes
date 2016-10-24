from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product,Wish
from ..login_reg_app.models import User

# Create your views here.
def index(request):
    if 'user' in request.session:
        return redirect('/dashboard')
    else:
        return redirect('/main')

def show_dashboard(request):
    if 'user' in request.session:
        currentUser = User.objects.get(uname = request.session['user']['uname'])
        context = {
          "mywishes" : Wish.objects.filter(user = currentUser),
          "otherwishes" : Wish.objects.exclude(user = currentUser)
        }
        return render(request, 'wishList/index.html',context)
    else:
        return redirect('/')

def show_main(request):
    return render(request, 'login_reg_app/index.html')

def show_create(request):
    if 'user' in request.session:
        context = {
          "products" : Product.objects.all().order_by('-updated_at')
        }
        return render(request, 'wishList/create.html', context)
    else:
        return redirect('/')

def create(request):
    if 'user' in request.session:
        currentUser = User.objects.get(uname = request.session['user']['uname'])
        #check if the product already exists - in this case reference the already existing product
        if not Product.objects.filter(name = request.POST['product']).exists():
            validatedProduct = Product.objects.create(name = request.POST['product'], description = request.POST['desc'])
        else:
            messages.error(request, "This product has already been created - we will go ahead and reference the existing product. You might loose your custom description.", extra_tags='creating_product')
            validatedProduct = Product.objects.get(name = request.POST['product'])
        if Wish.objects.filter(user=currentUser,product=validatedProduct).exists():
            # show error message
            messages.error(request, "Sorry, this product already exists in your wishlist.", extra_tags='creating_product')
        else:
            wishlist = Wish.objects.create(user = currentUser, product = validatedProduct)

        return redirect('/wish_item/create')
    else:
        return redirect('/')

def view_item(request,id):
    if 'user' in request.session:
        # get the product name and display the context
        currentproduct = Product.objects.get(id=id)
        wishers = Wish.objects.filter(product=currentproduct)
        context = {
          'product' : currentproduct,
          'wishers' : wishers
        }
        return render(request,'wishList/view.html',context)
    else:
        return redirect('/')

def add_product_to_mylist(request,id,username):
    if 'user' in request.session:
        currentUser = User.objects.get(uname = request.session['user']['uname'])
        currentproduct = Product.objects.get(id=id)
        removeuser = User.objects.get(uname=username)
        if not Wish.objects.filter(product=currentproduct).filter(user=currentUser).exists():
            wishlist = Wish.objects.create(user = currentUser, product = currentproduct)
            wishlist = Wish.objects.filter(user = removeuser, product = currentproduct).delete()

            return redirect('/')
        else:
            messages.error(request, "Sorry, this product already exists in your wishlist.", extra_tags='dashboard')
            return redirect('/')
    else:
        return redirect('/')

def remove_product_from_mylist(request,id):
    if 'user' in request.session:
        currentUser = User.objects.get(uname = request.session['user']['uname'])
        currentproduct = Product.objects.get(id=id)
        if Wish.objects.filter(product=currentproduct).filter(user=currentUser).exists():
            wishlist = Wish.objects.get(product=currentproduct,user=currentUser).delete()
            return redirect('/')
        else:
            messages.error(request, "Sorry, this product does not belong in your wishlist.", extra_tags='dashboard')
            return redirect('/')
    else:
        return redirect('/')

def delete_product(request,id):
    if 'user' in request.session:
        # Perform delete operation where we have to fetch all the users with the
        #wish_item and then delete each one of the item and then delete the product from
        # the products table assuming the author of the product is the logged in user
        return redirect('/')
    else:
        return redirect('/')
