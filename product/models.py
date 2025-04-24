from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Category(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField(blank=True,null=True)

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.name}/'

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    description=models.TextField(blank=True,null=True)
    price=models.DecimalField(max_digits=8,decimal_places=2)
    stock=models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.name}/{self.name}/'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Clear cache when product changes
        from .caching import invalidate_product_cache
        invalidate_product_cache(self.id)


@receiver([post_save, post_delete], sender=Product)
def clear_product_cache(sender, instance, **kwargs):
    instance.invalidate_product_cache(instance.id)
