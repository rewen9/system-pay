from django.contrib import admin
from backend.users.models import Users
from backend.admin import ADMIN_SITE

@admin.register(Users, site=ADMIN_SITE)
class usersAdmin(admin.ModelAdmin):
    model = Users
    list_display = ('name', 'company', 'balance', 'balance_currency')
    list_filter = ('name',)