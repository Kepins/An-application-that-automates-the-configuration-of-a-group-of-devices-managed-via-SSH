from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

from application.api.views.device import DeviceViewSet
from application.api.views.public_key import PublicKeyViewSet

router = DefaultRouter()
router.register(r"devices", DeviceViewSet, basename="devices")
router.register(r"keys", PublicKeyViewSet, basename="keys")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include((router.urls, "api"), namespace="api")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
