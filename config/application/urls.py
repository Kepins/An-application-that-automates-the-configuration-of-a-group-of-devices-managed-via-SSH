from django.urls import path

from .views import DeviceList

urlpatterns = [
    path("devices/", DeviceList.as_view()),
]
