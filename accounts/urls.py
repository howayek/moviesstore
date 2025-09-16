from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/',  auth_views.LoginView.as_view(template_name='accounts/login.html'), name='accounts.login'),
    path('logout/', auth_views.LogoutView.as_view(), name='accounts.logout'),
    path('orders/', views.orders, name='accounts.orders'),
]
