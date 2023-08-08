from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from rest_framework.routers import DefaultRouter

from application.api.views.device import DeviceViewSet
from application.api.views.public_key import PublicKeyViewSet
from application.api.views.group import GroupKeyViewSet

router = DefaultRouter()
router.register(r"devices", DeviceViewSet, basename="devices")
router.register(r"keys", PublicKeyViewSet, basename="keys")
router.register(r"groups", GroupKeyViewSet, basename="groups")

urlpatterns = [
    path("admin/", admin.site.urls),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    path('admin/', admin.site.urls),
path("api/", include((router.urls, "api"), namespace="api")),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


