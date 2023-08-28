from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from application.api.views.device import DeviceViewSet
from application.api.views.key_pair import KeyPairViewSet
from application.api.views.group import GroupKeyViewSet
from application.api.views.custom_user import RegisterView
from application.api.views.script import ScriptViewSet

router = DefaultRouter()
router.register(r"devices", DeviceViewSet, basename="devices")
router.register(r"keys", KeyPairViewSet, basename="keys")
router.register(r"groups", GroupKeyViewSet, basename="groups")
router.register(r"scripts", ScriptViewSet, basename="scripts")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api/", include((router.urls, "api"), namespace="api")),
    path("auth/register/", RegisterView.as_view(), name="register"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
