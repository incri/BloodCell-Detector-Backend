from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenCreateSerializer


class CustomTokenCreateView(TokenObtainPairView):
    serializer_class = CustomTokenCreateSerializer
