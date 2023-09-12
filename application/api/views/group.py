import uuid

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from application.api.serializers import RunSerializer
from application.api.serializers.group_serializer import (
    GroupSerializer,
    GroupAddDevicesSerializer,
    GroupRemoveDevicesSerializer,
)
from application.models.group import Group
from application.tasks import check_connection_task, run_script_on_device


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    serializer_add_devices = GroupAddDevicesSerializer
    serializer_remove_devices = GroupRemoveDevicesSerializer
    serializer_run_script = RunSerializer

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
        request_uuid = uuid.uuid4()

        group = self.get_object()
        for d in group.devices.all():
            check_connection_task.delay(group.id, d.id, request_uuid=request_uuid)

        return Response({"request_uuid": request_uuid}, status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["POST"])
    def run_script(self, request, pk):
        request_uuid = uuid.uuid4()
        group = self.get_object()
        serializer = RunSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        for d in group.devices.all():
            run_script_on_device.delay(
                group.id,
                d.id,
                serializer.validated_data["script"].pk,
                request_uuid=request_uuid,
            )

        return Response({"request_uuid": request_uuid}, status.HTTP_202_ACCEPTED)
