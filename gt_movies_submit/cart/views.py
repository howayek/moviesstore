from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from movies.models import Movie
from .models import Order, Item
from .utils import calculate_cart_total

def index(request):
    cart = request.session.get('cart', {})
    ids = list(cart.keys())
    movies_in_cart = Movie.objects.filter(id__in=ids) if ids else []
    total = calculate_cart_total(cart, movies_in_cart)
    return render(request, 'cart/index.html', {
        'template_data': {'title':'Cart', 'movies_in_cart': movies_in_cart, 'cart': cart, 'cart_total': total}
    })

def add(request, id):
    get_object_or_404(Movie, id=id)
    if request.method == 'POST':
        qty = request.POST.get('quantity', '1')
    else:
        qty = '1'
    cart = request.session.get('cart', {})
    cart[str(id)] = qty
    request.session['cart'] = cart
    return redirect('cart.index')

def clear(request):
    if request.method == 'POST':
        request.session['cart'] = {}
    return redirect('cart.index')

@login_required
def purchase(request):
    if request.method != 'POST':
        return redirect('cart.index')
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if not movie_ids:
        return redirect('cart.index')
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    order = Order.objects.create(user=request.user, total=cart_total)
    for m in movies_in_cart:
        Item.objects.create(order=order, movie=m, price=m.price, quantity=int(cart[str(m.id)]))
    request.session['cart'] = {}
    return render(request, 'cart/purchase.html', {'template_data': {'title':'Purchase complete', 'order_id': order.id}})
