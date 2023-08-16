from django.urls import path

from application.api.views.DeviceList import DeviceList

urlpatterns = [
    path("devices/", DeviceList.as_view()),
]
