
from django.shortcuts import render, redirect
from .models import Product


def home(request):
    products = Product.objects.all()
    return render(request, 'main/home.html', {'products': products})


def add_product(request):
    if request.method == 'POST':
        product = Product(
            name=request.POST['name'],
            price=request.POST['price'],
            category=request.POST['category'],
            image_url=request.POST['image_url'],
            description=request.POST['description']
        )
        product.save()
        return redirect('home')

    return render(request, 'main/form.html')


def edit_product(request, pk):
    product = Product.objects.get(id=pk)

    if request.method == 'POST':
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.category = request.POST['category']
        product.image_url = request.POST['image_url']
        product.description = request.POST['description']
        product.save()
        return redirect('home')

    return render(request, 'main/form.html', {'product': product})


def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('home')


def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    key = str(pk)
    cart[key] = cart.get(key, 0) + 1
    request.session['cart'] = cart
    return redirect('home')


def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    key = str(pk)

    if key in cart:
        cart[key] = cart[key] - 1

        if cart[key] == 0:
            del cart[key]

    request.session['cart'] = cart
    return redirect('cart')


def cart(request):
    cart_data = request.session.get('cart', {})
    items = []
    total = 0

    for pk in cart_data:
        product = Product.objects.get(id=pk)
        quantity = cart_data[pk]
        subtotal = product.price * quantity
        total = total + subtotal

        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'main/cart.html', {
        'items': items,
        'total': total
    })
