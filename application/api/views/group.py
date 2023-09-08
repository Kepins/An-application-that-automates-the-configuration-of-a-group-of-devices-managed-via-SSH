from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from application.api.serializers.group_serializer import (
    GroupSerializer,
    GroupAddDevicesSerializer,
    GroupRemoveDevicesSerializer,
)
from application.models.group import Group
from application.tasks import check_connection


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    serializer_add_devices = GroupAddDevicesSerializer
    serializer_remove_devices = GroupRemoveDevicesSerializer

    def get_serializer_class(self):
        if self.action == "add_devices":
            return self.serializer_add_devices
        if self.action == "remove_devices":
            return self.serializer_remove_devices
        return self.serializer_class

    @action(detail=True, methods=["PATCH"])
    def add_devices(self, request, pk):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"])
    def remove_devices(self, request, pk):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def check_connection(self, request, pk):

        group = self.get_object()
        for d in group.devices.all():
            check_connection.delay(group.id, d.id)

        return Response(None, status.HTTP_202_ACCEPTED)
