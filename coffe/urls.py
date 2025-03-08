from django.urls import path
from . import views
urlpatterns = [
    path('',views.start),
    path('buy',views.buy), 
    path('buying',views.confirm)
]