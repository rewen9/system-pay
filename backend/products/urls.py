from rest_framework import routers
from backend.products.views import ProductsViewSet

router = routers.SimpleRouter()

router.register(r'products', ProductsViewSet, basename='products')
urlpatterns = router.urls
