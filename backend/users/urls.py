from rest_framework import routers

from backend.users.views import RegisterView, LogViewSet

router = routers.SimpleRouter()

router.register(r'users', RegisterView, basename='users')
router.register(r'users/log', LogViewSet, basename='log')
urlpatterns = router.urls
