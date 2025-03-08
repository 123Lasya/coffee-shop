from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from django.contrib import messages
from .models import coffe
# Create your views here.
def start(request):
    d= coffe.objects.all()
    return render(request,'home.html',{'dict':d})
def buy(request):
    n = request.GET.get('id')
    if n is None:
        return redirect("/account/login") 
    else:    
        info = get_object_or_404(coffe, id=n)
        extra=coffe.objects.filter(Q(name__startswith=info.name[0]) | Q(price=info.price) | Q(id=(info.id+1)))
        return render(request,'coffeinfo.html',{'i':info ,'e':extra})
def confirm(request):
    return render(request,'confirmorder.html')