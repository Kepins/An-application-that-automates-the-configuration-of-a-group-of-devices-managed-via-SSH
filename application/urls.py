from django.urls import path

from application.api.views.DeviceDetail import DeviceDetail
from application.api.views.DeviceList import DeviceList

urlpatterns = [
    path("devices/", DeviceList.as_view()),
    path("devices/<int:pk>", DeviceDetail.as_view()),
]
