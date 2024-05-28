from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

# Define the default router
router = routers.DefaultRouter()

# Register the main endpoints
router.register("hospital", views.HospitalViewSet)

# Create nested routers
hospital_router = routers.NestedDefaultRouter(
    router, "hospital", lookup="hospital"
)

# Combine all URLs
urlpatterns = (
    router.urls + hospital_router.urls
)
