"""Центральный модуль для всей админки. """

from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group


class SystempayAdminSite(AdminSite):
    """Переопределенный AdminSite с целью изменения названия админки. """

    # Текст для <title>.
    site_title = 'Панель управления системой транзакций'

    # Текст для <h1> на каждой странице.
    site_header = 'Панель управления системой транзакций'

    # Текст на главной странице.
    index_title = 'Администрирование систем транзакций'


ADMIN_SITE = SystempayAdminSite()
ADMIN_SITE.register(Group, GroupAdmin)
ADMIN_SITE.register(get_user_model(), UserAdmin)
