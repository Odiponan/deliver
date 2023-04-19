from django.contrib import admin
from django.urls import path, include
from . import views
from .views import Dashboard, OrderDetails

urlpatterns = [
    path('',views.home, name="home"),
    path('signUp',views.signup, name="signup"),
    path('signIn',views.signin, name="signin"),
    path('signOut',views.signout, name="signout"),
    path('activate/<uidb64><token',views.activate, name="activate"),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('order/<int:pk>/', OrderDetails.as_view,name='order-details'),
    path('customer/', include('customer.html'))

]
