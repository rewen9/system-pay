from django.contrib import admin
from backend.transactions.models import Transactions
from backend.admin import ADMIN_SITE

@admin.register(Transactions, site=ADMIN_SITE)
class TransactioionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'amount', 'currency', 'status', 'created_at']
    list_filter = ['customer']