from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CollectViewSet, CustomUserViewSet, PaymentViewSet

router = DefaultRouter()

router.register("collect", CollectViewSet)
router.register(
    r"collect/(?P<collect_id>\d+)/payment", PaymentViewSet, basename="payments"
)
router.register("users", CustomUserViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]
