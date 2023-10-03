from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..serializers.register_serializer import RegisterSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def user_exists(request):
    if User.objects.exists():
        return Response({"exists": True}, status=200)
    return Response({"exists": False}, status=200)
