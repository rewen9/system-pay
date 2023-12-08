from django.db import models
from backend.users.models import Users, Log
from backend.products.models import Products

class Transactions(models.Model):
    STATUS_NEW = 'NEW'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_REJECTED = 'REJECTED'
    
    STATUS_CHOICES = (
        (STATUS_NEW, 'New'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_REJECTED, 'Rejected'),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text='Сумма',
    )
    currency = models.CharField(
        max_length=3,
        choices=Users.CURRENCY_CHOICES,
        default=Users.CURRENCY_RUB,
        help_text='Валюта',
    )  # Assuming RUB or USD
    customer = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='transactions',
        null=True,
        blank=True,
        help_text='Пользователь',
    )
    
    # Товар
    product = models.ForeignKey(
        Products,
        on_delete=models.DO_NOTHING,
        related_name='product_transactions',
        null=True,
        help_text='Товар',
    )
    product_quantity = models.IntegerField(
        default=1,
        null=True,
        blank=True,
        help_text='Количество покупаемого продукта',
    )

    reason_reject = models.ForeignKey(
        'Reasons',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        help_text='Причина отклонения',
    )
    
    @classmethod
    def create_transaction_new(cls, request, customer):
        
        customer_id = request.query_params.get('customer_id')
        amount = request.query_params.get('amount')
        currency = request.query_params.get('currency')
        product_quantity = request.query_params.get('product_quantity') 
        product_id = request.query_params.get('product') 
        
        product = Products.objects.filter(id__in=product_id).first()
        customer = Users.objects.filter(id=customer_id).first()
        transaction = cls(
            customer=customer,
            amount=amount, 
            currency=currency,
            product=product,
            product_quantity=product_quantity
        )
        
        transaction.save()

        customer.balance -= int(amount)
        customer.save(update_fields=['balance'])

        transaction.status = cls.STATUS_COMPLETED
        transaction.save(update_fields=['status'])
        
        log_entry = Log.objects.create(
            details=f"Transaction ID: {transaction.id}, Amount: {amount} {currency}",
        )
        log_entry.customer.set([customer])
        
        return transaction
    
    class Meta:
        app_label = 'transactions'
    def __str__(self):
        return f"{self.status} - {self.amount} {self.currency}"
    
class Reasons(models.Model):
    
    CHOISE_NOT_FUNDS = 'M'
    CHOISE_CANCELLED = 'C'
    CHOICE_NOT_QUANTITY = 'Q'
    
    CHOICES_REASONS = (
        (CHOISE_NOT_FUNDS, 'Недостаточно средств'),
        (CHOISE_CANCELLED, 'Отменено пользователем'),
        (CHOICE_NOT_QUANTITY, 'Недостаточное количество'),
    )
    
    reason = models.CharField(
        choices=CHOICES_REASONS,
        help_text='Причина отклонения',
        default=CHOISE_NOT_FUNDS,
    )
    description = models.CharField(
        max_length=255,
        help_text='Причина отклонения',
        null=True,
        blank=True,
    )
    transact = models.ForeignKey(
        Transactions,
        on_delete=models.DO_NOTHING,
        help_text='Транзакция',
    )
    
    class Meta:
        app_label = 'transactions'
    def __str__(self):
        return f"{self.reason}"
    