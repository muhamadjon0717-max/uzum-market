
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Product


def home(request):
    # Автоматически добавляем демонстрационные товары
    if not Product.objects.exists():
        products = [
            ("iPhone 16", 11500000, "Телефоны",
             "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=600"),
            ("Наушники JBL", 450000, "Электроника",
             "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600"),
            ("Кроссовки Nike", 850000, "Одежда",
             "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600"),
            ("Умные часы", 650000, "Электроника",
             "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600"),
            ("Ноутбук", 7500000, "Компьютеры",
             "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600"),
            ("Фотоаппарат", 3200000, "Электроника",
             "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=600"),
            ("Рюкзак", 250000, "Аксессуары",
             "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600"),
            ("Кресло", 1200000, "Дом",
             "https://images.unsplash.com/photo-1503602642458-232111445657?w=600"),
        ]

        for name, price, category, image in products:
            Product.objects.create(
                name=name,
                price=price,
                category=category,
                image_url=image,
            )

    products = Product.objects.all().order_by("-id")
    search = request.GET.get("q", "")
    category = request.GET.get("category", "")

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(category__icontains=search)
        )

    if category:
        products = products.filter(category=category)

    categories = Product.objects.values_list(
        "category", flat=True
    ).distinct()

    cart = request.session.get("cart", {})
    cart_count = sum(cart.values())

    return render(request, "main/home.html", {
        "products": products,
        "categories": categories,
        "search": search,
        "selected_category": category,
        "cart_count": cart_count,
    })


def add_product(request):
    if request.method == "POST":
        Product.objects.create(
            name=request.POST.get("name", ""),
            price=int(request.POST.get("price", 0)),
            category=request.POST.get("category", "Другие"),
            image_url=request.POST.get("image_url", ""),
            description=request.POST.get("description", ""),
        )
        return redirect("home")

    return render(request, "main/form.html", {"title": "Добавить товар"})


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.name = request.POST.get("name", "")
        product.price = int(request.POST.get("price", 0))
        product.category = request.POST.get("category", "Другие")
        product.image_url = request.POST.get("image_url", "")
        product.description = request.POST.get("description", "")
        product.save()
        return redirect("home")

    return render(request, "main/form.html", {
        "title": "Редактировать товар",
        "product": product,
    })


def delete_product(request, pk):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=pk)
        product.delete()

    return redirect("home")


def add_to_cart(request, pk):
    if request.method == "POST":
        get_object_or_404(Product, pk=pk)
        cart = request.session.get("cart", {})
        key = str(pk)
        cart[key] = cart.get(key, 0) + 1
        request.session["cart"] = cart

    return redirect("home")


def remove_from_cart(request, pk):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        key = str(pk)

        if key in cart:
            cart[key] -= 1
            if cart[key] <= 0:
                del cart[key]

        request.session["cart"] = cart

    return redirect("cart")


def cart(request):
    cart_data = request.session.get("cart", {})
    items = []
    total = 0

    for pk, quantity in cart_data.items():
        product = Product.objects.filter(pk=pk).first()
        if product:
            subtotal = product.price * quantity
            total += subtotal
            items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            })

    return render(request, "main/cart.html", {
        "items": items,
        "total": total,
    })
