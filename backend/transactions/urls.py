from rest_framework import routers

from backend.transactions.views import TransactionsView

router = routers.SimpleRouter()

router.register(r'transactions', TransactionsView, basename='transactions')
urlpatterns = router.urls
