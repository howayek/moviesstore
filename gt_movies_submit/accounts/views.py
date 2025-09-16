from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
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
