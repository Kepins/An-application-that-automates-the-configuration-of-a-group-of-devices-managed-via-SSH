from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

from application.api.views.device import DeviceViewSet
from application.api.views.public_key import PublicKeyViewSet
from application.api.views.group import GroupKeyViewSet
from application.api.views.script import ScriptDetailAPIView, ScriptListCreateAPIView

router = DefaultRouter()
router.register(r'scripts', ScriptListCreateAPIView, basename='script-list-create')
router.register(r'scripts', ScriptDetailAPIView, basename='script-detail')
router.register(r"devices", DeviceViewSet, basename="devices")
router.register(r"keys", PublicKeyViewSet, basename="keys")
router.register(r"groups", GroupKeyViewSet, basename="groups")

urlpatterns = [
    path('admin/', admin.site.urls),
path("api/", include((router.urls, "api"), namespace="api")),
    path('api-token-auth/', TokenObtainPairView.as_view()),
    path('api-token-refresh/', TokenRefreshView.as_view()),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


