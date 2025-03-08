from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
class coffe(models.Model):
    name=models.TextField(max_length=500)
    decription=models.TextField(max_length=100000)
    image=models.ImageField(upload_to='imgs')
    price=models.IntegerField()
    offer=models.BooleanField(default=False )
class cartitem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    coffeid=models.IntegerField(default=0)
    name=models.TextField(max_length=500,default='coffee')
    image=models.ImageField(upload_to='imgs',default='images/img-1') 
    price=models.IntegerField(default=0)
    offer=models.BooleanField(default=False )
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'coffeid'], name='unique_parent_child_value')
        ]
class orders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    coffeid=models.IntegerField(default=0)
    name=models.TextField(max_length=500,default='coffee')
    image=models.ImageField(upload_to='imgs',default='images/img-1') 
    price=models.IntegerField(default=0)
    quantity=models.IntegerField(default=0)
    offer=models.BooleanField(default=False )
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered')
    ]
    orderstatus = models.CharField(default="Pending",choices=ORDER_STATUS_CHOICES,max_length=20)
    