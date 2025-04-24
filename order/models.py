from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


from product.models import Product

from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Customer(AbstractUser):
    address=models.TextField(blank=True,null=True)
    phone=models.CharField(max_length=13,blank=True,null=True)
    Gender=models.CharField(max_length=20,blank=True,null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customer_groups', 
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customer_user_permissions',  
        blank=True,
        help_text='Specific permissions for this user.'
    )

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    )
    
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_total(self):
        self.total_price = sum(item.get_total() for item in self.items.all())
        self.save()

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"
    

@receiver(post_save, sender=Order)
def order_status_update(sender, instance, **kwargs):
    if kwargs.get('created', False):
        return
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"order_{instance.id}",
        {
            'type': 'order_update',
            'status': instance.status,
            'order_id': instance.id
        }
    )

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def get_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"