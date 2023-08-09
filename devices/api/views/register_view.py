from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny

from ..serializers.register_serializer import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
