from django.db import models
from backend.users.models import Users, Log


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
    )
    currency = models.CharField(
        max_length=3,
        choices=Users.CURRENCY_CHOICES,
        default=Users.CURRENCY_RUB,
    )  # Assuming RUB or USD

    customer = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='transactions',
        null=True,
        blank=True,
    )

    @classmethod
    def create_transaction_new(cls, customer_id, amount, currency):
        customer = Users.objects.filter(id=customer_id).first()
        transaction = cls(
            customer=customer,
            amount=amount, 
            currency=currency,
        )
        transaction.save()

        customer.balance += int(amount)
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