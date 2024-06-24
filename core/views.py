from rest_framework_simplejwt.views import TokenObtainPairView
from djoser.views import UserViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from lab.pagination import DefaultPagination
from .serializers import CustomTokenCreateSerializer, UserSerializer


class CustomTokenCreateView(TokenObtainPairView):
    serializer_class = CustomTokenCreateSerializer


class CustomUserViewSet(UserViewSet):
    pagination_class = DefaultPagination
    serializer_class = UserSerializer

    filter_backends = [
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    ]

    search_fields = ["username", "email"]
    ordering_fields = ["username"]
