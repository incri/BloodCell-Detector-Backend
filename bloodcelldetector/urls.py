"""
URL configuration for bloodcelldetector project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from core.views import (
    CustomTokenCreateView,
    CustomUserViewSet,
)

#comments
admin.site.site_header = "BCD Admin Dashboard"
admin.site.index_title = "Admin"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", include("lab.urls")),
    path("auth/jwt/create/", CustomTokenCreateView.as_view(), name="custom_register"),
    path(
        "auth/users/",
        CustomUserViewSet.as_view({"get": "list", "post": "create"}),
        name="user-list",
    ),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
