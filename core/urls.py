from django.urls import path, include
from rest_framework import routers

from core.views import QuotesViewSet, UserViewSet

router = routers.DefaultRouter()

router.register(r"quotes", QuotesViewSet, basename="quotes")
router.register(r"users", UserViewSet, basename="users")


app_name = "core"
urlpatterns = [
    path("", include(router.urls)),
]
