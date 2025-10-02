from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .forms import CustomUserCreationForm, CustomErrorList
from cart.models import Order

def signup(request):
    if request.method == 'GET':
        return render(request, 'accounts/signup.html', {'template_data': {'title':'Sign Up', 'form': CustomUserCreationForm()}})
    form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
    if form.is_valid():
        form.save()
        return redirect('home.index')
    return render(request, 'accounts/signup.html', {'template_data': {'title':'Sign Up', 'form': form}})

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/orders.html', {'template_data': {'title':'My Orders', 'orders': orders}})

@login_required
def subscription(request):
    agg = Order.objects.filter(user=request.user).aggregate(total=Sum('total'))
    spent = agg['total'] or 0
    if spent < 15:
        level = 'Basic'
        blurb = 'Less than $15 spent.'
    elif spent < 30:
        level = 'Medium'
        blurb = 'Between $15 and $30.'
    else:
        level = 'Premium'
        blurb = 'More than $30.'
    return render(request, 'accounts/subscription.html', {
        'template_data': {'title': 'My Subscription'},
        'spent': spent, 'level': level, 'blurb': blurb
    })
