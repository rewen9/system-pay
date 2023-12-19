from django.db import models
from backend.users.managers import LogsAuthorizedManager

class Users(models.Model):
    """Модель зарегистрированных пользователей."""
    CURRENCY_RUB = 'RUB'
    CURRENCY_USD = 'USD'
    CURRENCY_CHOICES = (
        (CURRENCY_RUB, 'RUB'),
        (CURRENCY_USD, 'USD'),
    )
    
    name = models.CharField(
        max_length=100
    )
    company = models.CharField(
        max_length=100
    )
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
    )
    balance_currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
    ) 

    def __str__(self):
        return f"{self.name} - {self.balance} {self.balance_currency}"
    
    class Meta:
        app_label = 'users'
        verbose_name = 'Пользователь'
        
    def register(js_data: dict):
        """Регистрация пользователя."""
        name = js_data.get('name')
        company = js_data.get('company') 
        balance = js_data.get('balance') or 0
        currency = js_data.get('balance_currency') or Users.CURRENCY_RUB
        
        # Создание пользователя в модели Users
        Users.objects.create(
            name=name, 
            company=company, 
            balance=balance, 
            balance_currency=currency,
        )

   
class Log(models.Model):
    """Описывает лог действий пользователя."""

    REGISTER_SUCCESS_USER = 0
    REGISTER_FAILED_USER = 1
    
    REGISTER_ACTION_FLAG_CHOICES = (
        (REGISTER_SUCCESS_USER, 'Успешная регистрация пользователя'),
        (REGISTER_FAILED_USER, 'Неудачная попытка регистрации пользователя'),
    )
    customer = models.ManyToManyField(
        Users,
        related_name='logs',
        blank=True,
    )
    action_time = models.DateTimeField(
        'Время действия', 
        auto_now_add=True,
    )
    action_description = models.TextField(
        'Описание действия', 
        blank=True,
        choices=REGISTER_ACTION_FLAG_CHOICES,
    )
    details = models.TextField(
        'Детали',
        blank=True,
        
    )
    Authorized = LogsAuthorizedManager()


    def __str__(self):
        return str(self.pk)

