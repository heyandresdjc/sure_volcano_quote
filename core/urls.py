from django.urls import path, include
from rest_framework import routers

from core.views import QuotesViewSet

router = routers.DefaultRouter()

router.register('quotes', QuotesViewSet, basename="quotes")

app_name = 'core'
urlpatterns = [
    path('', include(router.urls)),
]
