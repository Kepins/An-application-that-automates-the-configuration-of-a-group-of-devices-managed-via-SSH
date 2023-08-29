from rest_framework.views import APIView
from rest_framework.response import Response

from application.api.serializers.run_serializer import RunSerializer
from application.tasks.run_script import run_script_on_device


class RunScriptAPIView(APIView):
    def post(self, request, format=None):
        serializer = RunSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group = serializer.validated_data["group"]
        for device in group.devices.all():
            run_script_on_device.delay(
                group=group.id,
                device=device.id,
                script=serializer.validated_data["script"].id,
            )

        return Response(serializer.data)
