from rest_framework import generics, status
from rest_framework.response import Response


from application.api.serializers.DeviceSerializer import DeviceSerializer
from application.api.serializers.PublicKeySerializer import PublicKeySerializer
from application.models.Device import Device
from application.models.PublicKey import PublicKey


class DeviceList(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data={"name": request.data["name"], "hostname": request.data["hostname"]},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        if (
            "key_content" in request.data
            and not PublicKey.objects.filter(
                key_content=request.data["key_content"]
            ).exists()
        ):
            public_key = PublicKeySerializer(
                data={"key_content": request.data["key_content"]}
            )
            public_key.is_valid(raise_exception=True)
            public_key.save()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
