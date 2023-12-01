from django.urls import include, path

urlpatterns = [
    path('products/', include('backend.products.urls')),
    path('transactions/', include('backend.transactions.urls')),
    path('users/', include('backend.users.urls')),
]
