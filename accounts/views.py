from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from coffe.models import coffe,cartitem,orders
from django.contrib.auth.models import User,auth
from django.db.models.signals import post_save
from django.dispatch import receiver
from coffe.models import Profile

# Create your views here.
def reg(request):
    if request.method=='POST':
        f=request.POST['firstname']
        l=request.POST['lastname']
        u=request.POST['username']
        p=request.POST['password']
        e=request.POST['emailid']
        a=request.POST['address']
        pn=request.POST['phonenumber']
        exist=User.objects.filter(first_name=f, email=e).exists()
        if exist:
            messages.info(request,"The user is already existed")
            return render(request,'register.html')
        u=User.objects.create_user(password=p,username=u,first_name=f,last_name=l,email=e)
        o= Profile(user=u,address=a,phone_number=pn)
        o.save()
        return redirect("/")
    else:
        return render(request,'register.html')
def log(request):
    if request.method=='POST':
        u=request.POST['user_name']
        p=request.POST['password']
        user=auth.authenticate(password=p,username=u)
        if user is not None:
            auth.login(request,user)
            return redirect("/") 
        else:
            messages.info(request,"invalid information")
            return redirect('/account/login')
    else:
        return render(request,'login.html')
def logout(request):
    auth.logout(request)
    return redirect('/')
def cart(request):
    rc = request.GET.get('id')
    ru = request.GET.get('user')
    de=request.GET.get('del')
    userid = get_object_or_404(User, id=ru)  # Use get_object_or_404 to get the User object
    itemsexist= None
    if rc:
        reqid = get_object_or_404(coffe, id=rc)
        itemsexist=cartitem.objects.filter(user=userid,coffeid=rc).exists()
    if itemsexist:
        if de:
            item=get_object_or_404(cartitem,user=userid,coffeid=rc)
            item.delete()
        items=cartitem.objects.filter(user=userid)
        return render(request,'cart.html',{'d':items,'user':userid})
    elif rc:
       obj=cartitem(user=userid,coffeid=reqid.id,name=reqid.name,image=reqid.image,price=reqid.price,offer=reqid.offer)
       obj.save()
    items=cartitem.objects.filter(user=userid)
    return render(request,'cart.html',{'d':items,'user':userid})
def confirm(request):
    rc = request.GET.get('id')
    ru = request.GET.get('user')
    userid = get_object_or_404(User, id=ru)
    coffeid = get_object_or_404(coffe, id=rc)
    d=get_object_or_404(Profile, user=userid)
    pv=[]
    pr=[]
    ru = request.GET.get('user')
    use=get_object_or_404(User,id=ru)
    if request.method=='POST':
        q=request.POST['quantity']
        a=request.POST['address']
        p=request.POST['phone']
        if a == d.address and p == d.phone_number:
            ob=orders(user=userid,coffeid=rc,name=coffeid.name,image=coffeid.image,price=((coffeid.price)),offer=coffeid.offer,quantity=q)
            ob.save()
            items=orders.objects.filter(user=userid)
            for j in items:
                if(j.orderstatus=='Delivered'):
                    pv.append(j)
                else:
                    pr.append(j)
            return render(request,'ordertrack.html',{'past':pv,'present':pr,'user':use})
    items=orders.objects.filter(user=use)#send more than one
    for j in items:
        if(j.orderstatus=='Delivered'):
            pv.append(j)
        else:
            pr.append(j)
    if rc and ru:
        info={'rc':rc,'ru':ru}
        return render(request,'confirmorder.html',{'i':info})
    elif items:
        return render(request,'ordertrack.html',{'past':pv,'present':pr,'user':use})
    else:
        return redirect('/')
def ordertack(request):
    pv=[]
    pr=[]
    rc = request.GET.get('id')
    ru = request.GET.get('user')
    de = request.GET.get('del')
    d= request.GET.get('dup')
    use=get_object_or_404(User,id=ru)
    items=orders.objects.filter(user=use) 
    if rc and ru and de and d:
        itemsexist=orders.objects.filter(user=use,coffeid=rc).exists()
        if itemsexist:
            o=get_object_or_404(orders,user=use,coffeid=rc,id=d)
            o.delete()
            items=orders.objects.filter(user=use) 
    for j in items: 
        if(j.orderstatus=='Delivered'):
            pv.append(j)
        else:
            pr.append(j)
    if items:
        return render(request,'ordertrack.html',{'past':pv,'present':pr,'user':use})
    else:
        return redirect('/')      