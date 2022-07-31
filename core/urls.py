from django.urls import path
from rest_framework import routers


router = routers.DefaultRouter()

app_name = 'core'
urlpatterns = [
    path('', include(router.urls)),
]