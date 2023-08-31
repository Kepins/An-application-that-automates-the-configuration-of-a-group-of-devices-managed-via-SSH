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
                group_pk=group.id,
                device_pk=device.id,
                script_pk=serializer.validated_data["script"].id,
            )

        return Response(serializer.data)

    def get(self, request):
        import paramiko
        from io import StringIO
        from fabric import Connection

        key_content = """-----BEGIN OPENSSH PRIVATE KEY-----
        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
        -----END OPENSSH PRIVATE KEY----"""

        private_key = paramiko.RSAKey(file_obj=StringIO(key_content))
        c = Connection(
            host="192.168.0.10",
            user="tester",
            port=2222,
            connect_kwargs={"pkey": private_key},
        )

        result = c.run("#!/bin/bash\n echo HELLO", hide=True)
        print(result.stdout)
