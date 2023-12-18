from django.urls import include, path
from backend.admin import ADMIN_SITE

urlpatterns = [
    path('admin/', ADMIN_SITE.urls),
    path('products/', include('backend.products.urls')),
    path('transactions/', include('backend.transactions.urls')),
    path('users/', include('backend.users.urls')),
]
