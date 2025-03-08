from django.urls import path
from . import views
urlpatterns = [
    path('register', views.reg),
    path('login', views.log),
    path('logout', views.logout),
    path('cart',views.cart), 
    path('confirmorder',views.confirm),
    path('ordertack',views.ordertack),
]   