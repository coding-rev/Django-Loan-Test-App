from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

# Admin routes
router.register("", DatasetViewSet)

urlpatterns = [path("", include(router.urls))]
