from django.db import models

class Products(models.Model):
    """Товары в магазине"""
    name = models.CharField(
        max_length=250
    )
    
    class Meta:
        app_label = 'products'
    def __str__(self):
        return self.name

class Products_price(models.Model):
    """Цены на товары"""
    product = models.OneToOneField(
        Products,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    class Meta:
        app_label = 'products'
    def __str__(self):
        return self.price

class Products_count(models.Model):
    """Кол-во товаров в магазине"""
    product = models.OneToOneField(
        Products,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    class Meta:
        app_label = 'products'
        
    available_quantity = models.PositiveIntegerField()
    def __str__(self):
        return self.id